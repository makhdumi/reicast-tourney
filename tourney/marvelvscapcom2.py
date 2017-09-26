from reicast_reader import ReicastReader

class MarvelVsCapcom2(ReicastReader):

    # values from http://gamehacking.org/game/51908
    def __init__(self, pid=None):
        ReicastReader.__init__(self, pid, p1_health=0xC268760)