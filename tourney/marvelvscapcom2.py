from reicast_reader import ReicastReader


CHARACTER_CODES = {
    0x20: "Felicia",
    0x1c: "Megaman",
    0x38: "Captain Commando",
    0x07: "Wolverine2",
    0x2d: "Shuma Gorath",
    0x36: "Thanos",
    0x23: "Dan",
    0x02: "Guile",
    0x15: "Amingo",
    0x06: "Cyclops",
    0x39: "Wolverine1",
    0x2e: "War Machine",
    0x27: "Ken",
    0x1f: "B.B. hood",
    0x00: "Ryu ",
    0x14: "Sonson",
    0x16: "Marrow",
    0x08: "Psylock",
    0x2f: "Silver Samurai",
    0x2b: "Sabertooth",
    0x21: "Charlie",
    0x1e: "Akuma",
    0x01: "Zangief",
    0x13: "Ruby Heart",
    0x17: "Cable",
    0x09: "Ice man",
    0x28: "Gambit",
    0x35: "Blackheart",
    0x25: "Dhalsim",
    0x37: "Jin",
    0x04: "Anakaris",
    0x12: "Hayato",
    0x0b: "Captain America",
    0x0c: "Spiderman",
    0x29: "Juggernaut",
    0x31: "Spiral",
    0x26: "M. bison",
    0x03: "Morgan",
    0x22: "Sakura",
    0x10: "T. Baonne",
    0x0f: "Doctor Doom",
    0x0e: "Venom",
    0x2c: "Magneto",
    0x32: "Colossus",
    0x24: "Cammy",
    0x05: "Strider",
    0x11: "Jill",
    0x0a: "Rogue",
    0x0d: "Hulk",
    0x33: "Iron man",
    0x3a: "Servbot",
    0x1d: "Roll",
    0x1b: "Chun Li",
    0x30: "Omega Red",
    0x2a: "Storm",
    0x34: "Sentinel",
}

class MarvelVsCapcom2(ReicastReader):

    # values from http://gamehacking.org/game/51908
    def __init__(self, pid=None):
        ReicastReader.__init__(self, pid)

        player_offset = 0xb48
        character_offset = 0x5a4

        p1_c1_health = 0xc268760
        p1_c1_id = 0xc268760

        for p in range(1, 3):
            for c in range(1, 2):
                self._add_value("p%d_c%d_health" % (p, c),
                                p1_c1_health + player_offset * (p-1) + character_offset * (c-1), 4)
                self._add_value("p%d_c%d_id" % (p, c),
                                p1_c1_id + player_offset * (p-1) + character_offset * (c-1), 4)

                self._add_value("p%d_c%d_id" % (p,c), 0xc26886c + player_offset * (p-1), 4)