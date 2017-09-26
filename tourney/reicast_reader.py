from process_reader import ProcessReader
import subprocess
import re

class ReicastReader(ProcessReader):

    def __init__(self, pid=None, **entries):
        if pid is None:
            pid = int(subprocess.check_output(["pgrep", "reicast"]))

        exe = subprocess.check_output(["readlink", "-f", "/proc/%d/exe" % pid])
        maps = subprocess.check_output(["cat", "/proc/%d/maps" % pid])
        for line in maps.split("\n"):
            if "_vmem_MemInfo_ptr" in line:
                vmem_info_addr = int(re.split("\\s+", line)[0], 16)
                self.base_address = (ProcessReader.read_value(pid, vmem_info_addr + 8*0xC, 4)) & ~0xF

        if not self.base_address:
            raise Exception("Unable to find reicast process with symbol _vmem_MemInfo_ptr")

        ProcessReader.__init__(pid, **entries)

    def _add_value(self, name, address, length, is_int=True):
        offset = address & 0x0FFFFFF
        actual_address = self.base_address + offset
        ProcessReader._add_value(name, actual_address, length, is_int)