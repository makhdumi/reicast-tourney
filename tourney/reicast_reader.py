from process_reader import ProcessReader
import subprocess
import re

class ReicastReader(ProcessReader):

    def __init__(self, pid=None, **entries):
        if pid is None:
            pid = int(subprocess.check_output(["pgrep", "reicast"]))

        exe = subprocess.check_output(["readlink", "-f", "/proc/%d/exe" % pid]).split("\n")[0]
        objdump = subprocess.check_output(["objdump", "-x", exe])

        self.base_address = None
        for line in objdump.split("\n"):
            if "_vmem_MemInfo_ptr" in line:
                print line
                vmem_info_addr = int(re.split("\\s+", line)[0], 16)
                print "vmem_info = %x\n" % vmem_info_addr
                self.base_address = (ProcessReader.read_value(pid, vmem_info_addr + 0xC*4, 4)) & ~0xF

        if self.base_address is None:
            raise Exception("Unable to find reicast process with symbol _vmem_MemInfo_ptr")

        ProcessReader.__init__(self, pid, **entries)

    def _add_value(self, name, address, length, is_int=True):
        offset = address & 0x0FFFFFF
        actual_address = self.base_address + offset
        ProcessReader._add_value(self, name, actual_address, length, is_int)
