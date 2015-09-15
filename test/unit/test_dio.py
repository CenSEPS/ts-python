import unittest
from nose.tools import assert_raises
from mock import patch
import struct
from ts7250v2.dio import DIO
from ts7250v2.exceptions import TSDIOArgError

DATACORE_BIT_VALUE = (1 << 7)
DATACORE_BIT_DATA_DIR = (1 << 6)
SYSCON_BASE = 0x80004000


class TestDIO(unittest.TestCase):

    @patch('ts7250v2.dio.DIO._set_reg')
    @patch('ts7250v2._syscon.Syscon.__init__')
    def test_DIO_set_output(self, mock_init, mock_set_reg):
        """test the member DIO.DIO_set_output(dioName)"""
        # candidate for setup method
        d = DIO()
        # parameter definition for test
        pin = 'DIO_01'
        d.DIO_set_output(pin)
        mock_set_reg.assert_called_with(pin, DATACORE_BIT_VALUE | DATACORE_BIT_DATA_DIR)
        mock_init.asser_called_with(SYSCON_BASE)

    @patch('ts7250v2.dio.DIO._set_reg')
    @patch('ts7250v2._syscon.Syscon.__init__')
    def test_DIO_set_input(self, mock_init, mock_set_reg):
        """test the member DIO.DIO_set_input(dioName)"""
        d = DIO()
        pin = 'DIO_01'
        d.DIO_set_input(pin)
        mock_set_reg.assert_called_with(pin, DATACORE_BIT_DATA_DIR)
        mock_init.assert_called_with(SYSCON_BASE)

    @patch('ts7250v2.dio.DIO._set_reg')
    @patch('ts7250v2._syscon.Syscon.__init__')
    def test_DIO_set_high(self, mock_init, mock_set_reg):
        """test the member DIO.DIO_set_high(dioName)"""
        d = DIO()
        pin = 'DIO_01'
        d.DIO_set_high(pin)
        mock_set_reg.assert_called_with(pin, DATACORE_BIT_VALUE)
        mock_init.assert_called_with(SYSCON_BASE)

    @patch('ts7250v2.dio.DIO._set_reg')
    @patch('ts7250v2._syscon.Syscon.__init__')
    def test_DIO_set_low(self, mock_init, mock_set_reg):
        """test the member DIO.DIO_set_low(dioName)"""
        d = DIO()
        pin = 'DIO_01'
        d.DIO_set_low(pin)
        mock_set_reg.assert_called_with(pin, 0)
        mock_init.assert_called_with(SYSCON_BASE)

    def test_check_arg_dioName(self):
        """test the static method DIO._check_arg_dioName"""
        assert_raises(TSDIOArgError, DIO._check_arg_dioName, 5)
        assert_raises(TSDIOArgError, DIO._check_arg_dioName, '')
        assert_raises(TSDIOArgError, DIO._check_arg_dioName, 'DIO_02')
        DIO._check_arg_dioName('DIO_01')

    def test_check_arg_configBits(self):
        """test the static method DIO._check_arg_configBits"""
        assert_raises(TSDIOArgError, DIO._check_arg_configBits, 0x01)
        assert_raises(TSDIOArgError, DIO._check_arg_configBits, 'a')
        DIO._check_arg_configBits(0)
        DIO._check_arg_configBits(DATACORE_BIT_VALUE)
        DIO._check_arg_configBits(DATACORE_BIT_DATA_DIR)
        DIO._check_arg_configBits(DATACORE_BIT_VALUE | DATACORE_BIT_DATA_DIR)

    @patch('ts7250v2._syscon.Syscon._writeReg16')
    @patch('ts7250v2._syscon.Syscon.__init__')
    def test__set_reg(self, mock_init, mock_writeReg16):
        """test the method DIO._set_reg(dioName, configBits)"""
        # because of the above tests we don't need to worry about feeding bad data into
        # set reg... crosses fingers
        d = DIO()
        configBits = 0
        # DIO_MAP[dio_string] == 76
        dioString = 'DIO_01'
        dio = 76
        # DIO_REGISTER_OFFSET['DATACORE1'] == 0x3a
        v = struct.pack('<h', (dio-64) | configBits)
        d._set_reg(dioString, configBits)
        mock_writeReg16.assert_called_with(0x3a, v)
        configBits = DATACORE_BIT_VALUE
        v = struct.pack('<h', (dio-64) | configBits)
        d._set_reg(dioString, configBits)
        mock_writeReg16.assert_called_with(0x3a, v)
        configBits = DATACORE_BIT_DATA_DIR
        v = struct.pack('<h', (dio-64) | configBits)
        d._set_reg(dioString, configBits)
        mock_writeReg16.assert_called_with(0x3a, v)
        configBits = DATACORE_BIT_DATA_DIR | DATACORE_BIT_VALUE
        v = struct.pack('<h', (dio-64) | configBits)
        d._set_reg(dioString, configBits)
        mock_writeReg16.assert_called_with(0x3a, v)
        # patch the check methods so that you can verify DATACORE0 or DATACORE1 are used correctly
        # otherwise there are untested lines in _set_reg

    @patch('ts7250v2.dio.DIO._check_arg_dioName')
    @patch('ts7250v2.dio.DIO._check_arg_configBits')
    @patch('ts7250v2._syscon.Syscon.__init__')
    @patch('ts7250v2._syscon.Syscon._writeReg16')
    @patch('ts7250v2.dio.DIO_MAP')
    def test__set_reg_no_argCheck(self, mock_map, mock_writeReg16,
                                  mock_init, mock_check_configBits,
                                  mock_check_dioname):
        """test the method DIO._set_reg with the _check_arg_* methods mocked out"""
        d = DIO()
        dio = 60
        mock_map.__getitem__.return_value = dio
        offset = 0x36
        configBits = DATACORE_BIT_VALUE
        v = struct.pack('<h', dio | configBits)
        d._set_reg(dio, configBits)
        mock_writeReg16.assert_called_with(offset, v)

        dio = 76
        mock_map.__getitem__.return_value = dio
        offset = 0x3a
        v = struct.pack('<h', (dio-64) | configBits)
        d._set_reg(dio, configBits)
        mock_writeReg16.assert_called_with(offset, v)

    def test_DIO_read(self):
        """blah"""
        pass
