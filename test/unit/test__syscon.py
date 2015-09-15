import unittest
from mock import patch, MagicMock
from nose.tools import assert_raises
import struct

from ts7250v2._syscon import Syscon
from ts7250v2.exceptions import TSSysconError, TSSysconArgError
from os import O_RDWR, O_SYNC
from mmap import PAGESIZE, PROT_READ, PROT_WRITE, MAP_SHARED


class TestSyscon(unittest.TestCase):

    @patch('os.open')
    @patch('os.close')
    @patch('mmap.mmap')
    def test_constructor(self, mock_mmap, mock_os_close, mock_os_open):
        addr = 0x5
        size = PAGESIZE
        a_addr = addr - (addr % PAGESIZE)
        a_size = size + (addr - a_addr)
        fd = 5
        mock_os_open.return_value = fd
        s = Syscon(addr)
        mock_os_open.assert_called_with('/dev/mem', O_RDWR | O_SYNC)
        mock_mmap.assert_called_with(
            fd,
            a_size,
            flags=MAP_SHARED,
            prot=PROT_READ | PROT_WRITE,
            offset=a_addr
        )
        mock_os_close.assert_called_with(fd)
        # check argument parsing
        assert_raises(TSSysconArgError, Syscon, 'a')
        assert_raises(TSSysconArgError, Syscon, addr, size='a')
        # test  a generic failure from os.close
        mock_os_close.side_effect = OSError("OOPSIE")
        assert_raises(TSSysconError, Syscon, addr)
        mock_os_close.side_effect = None
        # test a generic failure from os.open
        mock_os_open.side_effect = OSError("oops")
        assert_raises(TSSysconError, Syscon, addr)
        mock_os_open.side_effect = None
        # test for a generic failure from mmap.mmap
        mock_mmap.side_effect = OSError('lol')
        assert_raises(TSSysconError, Syscon, addr)
        del s  # prevent PEP 8 problem with assigning but not using the variable s

    def test_constructor_unpriv_user(self):
        """Ensure that we cannot open /dev/mem normally (permission denied)"""
        addr = 0x5
        assert_raises(TSSysconError, Syscon, addr)

    @patch('os.open')
    @patch('os.close')
    @patch('mmap.mmap')
    def test__writeReg16(self, mock_mmap, mock_os_close, mock_os_open):
        addr = 0x5
        s = Syscon(addr)
        s.mapping = MagicMock()
        offset = 2
        assert_raises(TSSysconArgError, s._writeReg16, offset, 5)
        assert_raises(TSSysconArgError, s._writeReg16, offset, 'a')

        packedValue = struct.pack('<h', 0xCC)
        s._writeReg16(2, packedValue)
        s.mapping.__setitem__.assert_called_with(slice(offset, offset+2), packedValue)
