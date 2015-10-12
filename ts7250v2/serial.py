"""serial.py: handles serial port access from CPU uart to FPGA xuart"""
from serial import Serial
from config import SERIAL_DEVICES

# need a base class RS232 Serial?


class BaseSerial(Serial):
    # this sucker should call initialize so the mixin magic can work
    def __init__(self, port=None, baudrate=9600,
                 bytesize=8, parity='N', stopbits=1, timeout=None,
                 xonxoff=False, rtscts=False, writeTimeout=None,
                 dsrdtr=False, interCharTimeout=None):

        self.initialize()  # shit how to track portname for xuartmixin?
        super(BaseSerial, self).__init__(port=port, baudrate=baudrate,
                                         bytesize=bytesize, parity=parity,
                                         stopbots=stopbits, timeout=timeout,
                                         xonxoff=xonxoff, rtscts=rtscts, dsrdtr=dsrdtr,
                                         interCharTimeout=interCharTimeout)

        def initialize(self, *args, **kwargs):
            pass


class RS232SerialBase(Serial):
    RS232_DEVICES = {k: v['file'] for k, v in SERIAL_DEVICES.items() if v['proto'] == 'RS232'}

    def __init__(self, port=None, **kwargs):
        # do more checks on port... is it a name or a file?

        super(RS232SerialBase, self).__init__(port=port, **kwargs)

    def initialize(portNum):
        pass


class CPUSerial(RS232SerialBase):

    CPUSERIAL_DEVICE = 's0'

    def __init__(self, port=SERIAL_DEVICES[CPUSERIAL_DEVICE]['file'], baudrate=9600,
                 bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=False,
                 rtscts=False, writeTimeout=None, dsrdtr=False, interCharTimeout=None):

        super(CPUSerial, self).__init__(port=port, baudrate=baudrate,
                                        bytesize=bytesize, parity=parity,
                                        stopbots=stopbits, timeout=timeout,
                                        xonxoff=xonxoff, rtscts=rtscts, dsrdtr=dsrdtr,
                                        interCharTimeout=interCharTimeout)


class XUARTMixIn(object):
    def initialize(self, xuartName):
        pass
