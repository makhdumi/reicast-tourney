import ctypes as c

class iovec(c.Structure):
    _fields_ = [("iov_base", c.c_void_p), ("iov_len", c.c_size_t)]

class MemoryEntry:
    def __init__(self, address, length, name=None, is_int=True, transform_func=None):
        self.name = name
        self.address = address
        self.length = length
        self.is_int = is_int
        self.value = None
        self.transform_func = transform_func

    def get_value(self):
        print "calling with %d" % self.value
        if self.transform_func: self.transform_func(0)
        return self.transform_func(self.value) if self.transform_func else self.value

class ProcessReader:

    _c_process_vm_readv = None

    def __init__(self, pid, **entries):
        self.pid = pid
        self._entries = []
        for key in entries:
            self._add_value(key, entries[key].address, entries[key].length)

    def update(self):
        ProcessReader._read_values(self.pid, self._entries)
        for entry in self._entries:
            self.__dict__[entry.name] = entry.get_value()

    @staticmethod
    def read_value(pid, address, length, as_int=True):
        print "reading %x from process %d"  % (address, pid)
        entries = [MemoryEntry(address, length, is_int=as_int)]
        result = ProcessReader._read_values(pid, entries)[0].value
        return result

    @staticmethod
    def _read_values(pid, entries):
        n = len(entries)
        local = (iovec*n)()
        remote = (iovec*n)()
        total_bytes_expected = 0
        for i in range(n):
            remote[i].iov_base = c.c_void_p(entries[i].address)
            remote[i].iov_len = entries[i].length

            buf = (c.c_char*entries[i].length)()
            entries[i].buf = buf
            local[i].iov_base = c.cast(c.byref(buf), c.c_void_p)
            local[i].iov_len = entries[i].length

            total_bytes_expected += entries[i].length

        if not ProcessReader._c_process_vm_readv:
            ProcessReader._c_process_vm_readv = ProcessReader._get_process_vm_readv()
        nread = ProcessReader._c_process_vm_readv(pid, local, n, remote, n, 0)
        if nread != total_bytes_expected:
            raise Exception("Failed to read all iovec entries: %d vs expected %d" % (nread, total_bytes_expected))

        for i in range(n):
            if entries[i].is_int:
                entries[i].value = 0
                for j in range(entries[i].length):
                    print ord(entries[i].buf[j])
                    # ARMv7 is little-endian
                    entries[i].value |= (ord(entries[i].buf[j]) << (j*8))

            else:
                entries[i].value = entries[i].buf

        return entries

    def _add_value(self, name, address, length, is_int=True, transform_func=None):
        entry = MemoryEntry(address, length, name=name, is_int=is_int, transform_func=transform_func)
        self._entries.append(entry)
        self._c_entries = None

    @staticmethod
    def _get_process_vm_readv():
        libc = c.CDLL("libc.so.6")
        func = libc.process_vm_readv
        func.argtypes = [c.c_int, c.POINTER(iovec), c.c_ulong, c.POINTER(iovec), c.c_ulong, c.c_ulong]
        return func
