from _mmio import MMIO
from exceptions import TSDIOArgError
from config import DIO_REGISTER_OFFSET, SYSCON_BASE_ADDRESS
import struct


DIO_MAP = {
    'DIO_01': 76,
    'DIO_03': 77,
    'DIO_05': 78,
    'DIO_07': 79,
    'DIO_09': 80,
    'DIO_11': 81,
    'DIO_13': 82,
    'DIO_15': 83,
}
"""dict: maps DIO names with evgpio numbers

The evgpio numbers represent a small subset of the entire
evgpio space.
"""

DATACORE_BIT_DATA_DIR = (1 << 6)
"""uint: a single bit used for working with the EVGPIO Data Core registers"""
DATACORE_BIT_VALUE = (1 << 7)
"""uint: a single bit used for working with the EVGPIO Data Core registers"""
DATACORE_BIT_VALID_READ_DATA = (1 << 8)
"""uint: a single bit used for working with the EVGPIO Data Core revisters"""
MASKCORE_BIT_MASK_SET = (1 << 7)
"""uint: a signle bit used for working with the EVGPIO Mask Core registers"""

# The deal with config
# we're working with a 16 bit register
# | 15:9 | Reserved (write 0)
# |   8  | Valid Read Data (R/O - write 0)
# |   7  | Value
# |   6  | Data / not(Data Direction)
# |  5:0 | DIO number
#
# DIO number is limited to 5 bits, 0x1F
# We have 2 bits that are valid


class DIO(object):
    '''Software control of digital I/O

    Currently this class is compatible with the TS-7250-v2
    from Technologic Systems.

    For now it offers a similar interface to evgpioctl, but
    intentionally limited to the DIO ports exposed by TS-782
    that comes preinstalled in our computer cases.

    Arguments:
        TBD
    '''

    def __init__(self):
        # ensure consistent or specific state?
        # not now
        self.map = MMIO(SYSCON_BASE_ADDRESS)

    def _pick_register_offset(self, d):
        if d < 64:
            _data = DIO_REGISTER_OFFSET['DATACORE0']
            _mask = DIO_REGISTER_OFFSET['MASKCORE0']
        else:
            d -= 64
            _data = DIO_REGISTER_OFFSET['DATACORE1']
            _mask = DIO_REGISTER_OFFSET['MASKCORE1']

        return (d, _data, _mask)

    def DIO_set_output(self, dioName):
        """set the data direction of specified `dioName` to output

        Arguments:
            dio: an i/o port specified in::

                DIO_MAP.keys()

        Raises:
            TSDIOError

        """
        self._check_arg_dioName(dioName)
        (d, data_off, mask_off) = self._pick_register_offset(DIO_MAP[dioName])
        self.map.poke16(data_off, d | DATACORE_BIT_DATA_DIR | DATACORE_BIT_VALUE)

    def DIO_set_input(self, dioName):
        """set the data direction of specified `dioName` to input

        Arguments:
            dio: an i/o port specified in::

                DIO_MAP.keys()

        Raises:
            TSDIOError
        """
        self._check_arg_dioName(dioName)
        (d, data_off, mask_off) = self._pick_register_offset(DIO_MAP[dioName])
        self.map.poke16(data_off, d | DATACORE_BIT_DATA_DIR)

    def DIO_set_high(self, dioName):
        """set the specified pin to output high

        if the pin is currently in input mode, this command
        will still be reflected upon changing the pin mode
        to output

        Arguments:
            dioName

        Raises:
            TSDIOError
        """
        self._check_arg_dioName(dioName)
        (d, data_off, mask_off) = self._pick_register_offset(DIO_MAP[dioName])
        self.map.poke16(data_off, d | DATACORE_BIT_VALUE)

    def DIO_set_low(self, dioName):
        """set the specified pin to output low

        if the pin is currently in input mode, this command
        will still be reflected upon changing the pin mode
        to output

        Arguments:
            dioName - an i/o port specified in::

                DIO_MAP.keys()

        Raises:
            TSDIOError
        """
        self._check_arg_dioName(dioName)
        (d, data_off, mask_off) = self._pick_register_offset(DIO_MAP[dioName])
        self.map.poke16(data_off, d)

    def DIO_read(self, dioName):
        """read the specified pin

        Arguments:
            dioName - an i/o port specified in::

                DIO_MAP.keys()

        Returns:
                0 for low pin
                1 for high pin

        Raises:
            TSDIOError - bad dioName
            newexception - dio is not input?
        """
        # according evgpio.c there are several steps to reading an io pin
        # 1. Disable IRQ for pin (MASK_SET = 1)
        # 2. flush IRQ events  (Read data core reg until VALID_READ_DATA = 0
        # 3. Enable IRQ for pin (MASK_SET = 0)
        # 4. Read all IRQ events searching for pin number
        # 5. Return read VALUE bit (1 or 0) or 0
        value = 0
        self._check_arg_dioName(dioName)
        (d, data_off, mask_off) = self._pick_register_offset(DIO_MAP[dioName])

        # Step 1
        self.map.poke16(mask_off, d|MASKCORE_BIT_MASK_SET)
#        v = struct.pack("<h", d | MASKCORE_BIT_MASK_SET)
        print "Poke {} - {}".format(hex(mask_off), hex(d|MASKCORE_BIT_MASK_SET))
#        self.mapping[mask_off:mask_off+2] = v
        # Step 2
        while True:
            x = self.map.peek16(data_off)
#            v = self.mapping[data_off:data_off+2]
#            x = struct.unpack('<h', v)[0]
	    print "Peek {} - {}".format(hex(data_off), hex(x))
            if (x & DATACORE_BIT_VALID_READ_DATA)\
                != DATACORE_BIT_VALID_READ_DATA:
                    print "Flush complete"
                    break
	
        # Step 3
        self.map.poke16(mask_off, d & ~MASKCORE_BIT_MASK_SET)
#        v = struct.pack("<h", d & ~MASKCORE_BIT_MASK_SET)
        print "Poke {} - {}".format(hex(mask_off), hex(d& ~MASKCORE_BIT_MASK_SET))
#        self.mapping[mask_off:mask_off+2] = v

        # Step 4
        while True:
            x = self.map.peek16(data_off)
#            v = self.mapping[data_off:data_off+2]
#            x = struct.unpack('<h', v)[0]
    	    print "Peek {} - {}".format(hex(data_off), hex(x))
            if (x & DATACORE_BIT_VALID_READ_DATA)\
                != DATACORE_BIT_VALID_READ_DATA:
                    print "Value = {}".format(hex(value))
                    print "Read complete"
                    break
            else:
                if(x&0x1F) == d:
                    value = x & DATACORE_BIT_VALUE

	
        if value != 0:
            return 1
        else:
            return 0

    def _read(self, dio):
        value = 0
        if dio < 64:
            data_off = 0x36
            mask_off = 0x38
        else:
            data_off = 0x3a
            mask_off = 0x3c
            dio -= 64
        packed_data = struct.pack("<h", dio | 0x80)
        self.mapping[mask_off:mask_off+2] = packed_data

#         while True:
#             packed_data = self.mapping[data_off:data_off+2]
#             x  = struct.unpack("<h",packed_data)[0]
#             print hex(x)
#             if (x & 0x100) != 0x100:
#                 print "Flush complete"
#                 break
        
        packed_data = struct.pack("<h", dio & ~0x80)
        self.mapping[mask_off:mask_off+2] = packed_data

        while True:
            packed_data = self.mapping[data_off:data_off+2]
            x = struct.unpack("<h", packed_data)[0]
            print hex(x)
            if (x&0x100) != 0x100:
                print "Read complete"
                break
            else:
                if(x&0x7f) == dio:
                    value = x & 0x80

        return value

    @staticmethod
    def _check_arg_dioName(dioName):
        """Validates input for a common function argument: dioName

        Arguments:
            dioName - required to be a string and a member of::

                DIO_MAP.keys()

        Raises:
            TSDIOArgError - dioName is not valid
        """
        strerr_dioName = "Problem with argument `dioName` - "
        errno_dioName = 1
        if type(dioName) != str:
            raise TSDIOArgError(
                message=strerr_dioName+"Type {} != {}".format(type(dioName), type(str())),
                errno=errno_dioName
            )

        if dioName not in DIO_MAP.keys():
            raise TSDIOArgError(
                message=strerr_dioName+"'{}' not found in DIO_MAP.keys()".format(dioName),
                errno=errno_dioName
            )

    @staticmethod
    def _check_arg_configBits(configBits):
        """Validates input for a common function argument: configBits

        Arguments:
            configBits - required to be 1 of 3 possible values::

                0xC0,
                0x80,
                0x40

            or more readably::

                DATACORE_BIT_VALUE,
                DATACORE_BIT_DATA_DIR,
                DATACORE_BIT_VALUE|DATACORE_BIT_DATA_DIR

        Raises:
            TSDIOArgError - configBits is not valid
        """
        strerr_configBits = "Problem with argument `configBits` - "
        errno_configBits = 2
        if type(configBits) != int:
            raise TSDIOArgError(
                message=strerr_configBits+"Type {} != {}".format(type(configBits), type(int())),
                errno=errno_configBits
            )
        CONFIG_BIT_MASK = DATACORE_BIT_DATA_DIR | DATACORE_BIT_VALUE
        if (configBits & ~CONFIG_BIT_MASK) != 0:
            raise TSDIOArgError(
                message=strerr_configBits+"may only be DATACORE_BIT_DATA_DIR, \
                    DATACORE_BIT_VALUE, or DATACORE_BIT_DATA_DIR|DATACORE_BIT_VALUE",
                errno=errno_configBits
            )

    def _get_reg(self, dioName):
        """Reads dio input, regardless of dd state

        you are required for ensuring that the data direction of the specified DIO
        is input (0).

        Arguments:
            dioName: an i/o port specified in::

                DIO_MAP.keys()
        """
        raise NotImplemented

    # TODO: redo so it takes an EVGPIO # not a DIO Name?
    def _set_reg(self, dioName, configBits):
        """write dio|configBits to the appriopriate register

        Arguments:
            dioName: an i/o port specified in::

                DIO_MAP.keys()

            configBits: either of these two bits or BOTH.

                DATACORE_BIT_DATA_DIR
                DATACORE_BIT_VALUE

        Raises:
            TSDIOArgError - problem with dioName or configBits
        """
        self._check_arg_dioName(dioName)
        d = DIO_MAP[dioName]

        self._check_arg_configBits(configBits)

        if d < 64:
            offset = DIO_REGISTER_OFFSET['DATACORE0']
        else:
            offset = DIO_REGISTER_OFFSET['DATACORE1']
            d -= 64

        v = struct.pack('<h', d | configBits)
        self._writeReg16(offset, v)
