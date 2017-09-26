import unittest
from mock import MagicMock
from tourney.process_reader import ProcessReader, iovec, MemoryEntry
import ctypes as c

class ProcessReaderTests(unittest.TestCase):

    def fake_process_vm_readv(self, pid, local_ptr, local_n, remote_ptr, remote_n, flags):
        local_buf = (c.c_byte*local_ptr[0].iov_len)(local_ptr[0].iov_base)
        local_buf[0] = 0x10
        return 1

    def test_read_value_int32(self):
        reader = ProcessReader(1000)
        ProcessReader._c_process_vm_readv = self.fake_process_vm_readv
        value = reader.read_value(0x90513, 4)
        self.assertEqual(value, 0x10)

    def test_read_value_readvm_call(self):
        reader = ProcessReader(1000)
        mock = ProcessReader._c_process_vm_readv = MagicMock(return_value=1)
        reader.read_value(0x90513, 16)
        pid, local_ptr, local_n, remote_ptr, remote_n, flags = mock.call_args[0]

        self.assertEqual(pid, 1000)
        self.assertEqual(len(local_ptr), 1)
        self.assertEqual(local_n, 1)

        local_buf = (c.c_byte*16)(local_ptr[0].iov_base)
        self.assertEqual(len(local_buf), 16)
        self.assertEqual(local_ptr[0].iov_len, 16)

        self.assertEqual(len(remote_ptr), 1)
        self.assertEqual(remote_n, 1)
        self.assertEqual(remote_ptr[0].iov_base, 0x90513)
        self.assertEqual(remote_ptr[0].iov_len, 16)
