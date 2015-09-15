# import sys
import os
import mmap
# import struct
from exceptions import TSSysconError, TSSysconArgError
# import ctypes


class Syscon(object):
    def __init__(self, address, size=mmap.PAGESIZE):
        """Map memory section of memory at address `address of size 1s `size` bytes

        Arguments:
            address (integer): base address of memory region.
            size (integer): size of memory region (bytes).

        Returns:
            Syscon object

        Raises:
            TSSysconError: if an I/O or OS error occurs.
            TypeError: if `address` or `size` are incorrect type

        """
        if not isinstance(address, int) and not isinstance(address, long):
            raise TSSysconArgError(
                "Argument `address` should be of type int or long, not `{}`".format(
                    type(address)
                )
            )
        if not isinstance(size, int) and not isinstance(address, long):
            raise TSSysconArgError(
                "Argument `size` should be of type int, not `{}`".format(
                    type(size))
            )

        pagesize = mmap.PAGESIZE

        self._address = address
        self._size = size
        self._aligned_address = address - (address % pagesize)
        self._aligned_size = size + (address - self._aligned_address)

        try:
            fd = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
        except OSError as e:
            raise TSSysconError("Opening /dev/mem: " + e.message, e.errno)

        try:
            self.mapping = mmap.mmap(
                fd,
                self._aligned_size,
                flags=mmap.MAP_SHARED,
                prot=(mmap.PROT_READ | mmap.PROT_WRITE),
                offset=self._aligned_address
            )

        except OSError as e:
            raise TSSysconError("Mapping /dev/mem: " + e.message, e.errno)

        # test that we're using the correct device, 0x7250
#         x = self.peek16(0x00)
#         if x != 0x7250:
#             raise TSSysconError("Address {} is not equal to 0x7250 {}".format((self._address, x)))

        try:
            os.close(fd)
        except OSError as e:
            raise TSSysconError("Closing /dev/mem: " + e.message, e.errno)

    def _writeReg16(self, registerOffset, packedValue):
        # placeholder for registerOffset bound check

        if (type(packedValue) != str) or (len(packedValue) != 2):
            raise TSSysconArgError('invalid packedValue.')

        self.mapping[registerOffset:registerOffset+2] = packedValue
