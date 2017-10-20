from reicast_reader import ReicastReader


CHARACTER_CODES = {
    0x20: "Felicia",
    0x1c: "Megaman",
    0x38: "Captain Commando",
    0x07: "Wolverine [Adamantium]",
    0x2d: "Shuma Gorath",
    0x36: "Thanos",
    0x23: "Dan",
    0x02: "Guile",
    0x15: "Amingo",
    0x06: "Cyclops",
    0x39: "Wolverine [Bone]",
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

def get_char_name(id):
    return CHARACTER_CODES[id]

class State:
    Unknown, UnknownPaused, SetTimer, CheckTimer, MatchActive, MatchPaused, MatchDone = range(7)

class MarvelVsCapcom2(ReicastReader):

    def get_timer_value(self):
        return self.timer*120 + self.timer_part

    def next_state(self):
	print "current state = %d. paused? = %d" % (self.state, self.paused)
        if self.state == State.Unknown:
            if self.paused:
                self.state = State.UnknownPaused
            elif self.timer > 0:
                print "SET TIMER"
                self.state = State.SetTimer
            else:
                self.state = State.Unknown
        elif self.state == State.UnknownPaused:
            if self.paused:
                self.state = State.UnknownPaused
            else:
                self.state = State.Unknown
        elif self.state == State.SetTimer:
            print("WHAT THE FUCK?")
            # todo: change to match active
            self.time_check_start = self.get_timer_value()
            self.state = State.CheckTimer
            print("set timer=%s" % str(self.time_check_start))
        elif self.state == State.CheckTimer:
            timer_dec = self.get_timer_value() - self.time_check_start > 0
            if not timer_dec:
                self.state = State.Unknown
            else:
                self.state = State.MatchActive
        # match is active?
        elif self.state == State.MatchActive:
            if self.p1_c1_id == 0:
                self.state = State.Unknown
            if self.paused:
                self.state = State.MatchPaused
            if self.match_done:
                self.state = State.MatchDone
        elif self.state == State.MatchPaused:
            if self.paused:
                self.state = State.MatchPaused
            else:
                self.state = State.MatchActive
        elif self.state == State.MatchDone:
            print("MATCH COMPLETE!!!")
            self.state = 6
	print "next state = %d" % self.state
        

    def __init__(self, pid=None):
        ReicastReader.__init__(self, pid)
        self.state = 0

        self._add_value("timer", 0xc289620, 1, True, None)
        self._add_value("timer_part", 0xc289621, 1, True, None)

        self._add_value("match_done", 0xc289636, 1, True, None)

	self._add_value("paused", 0xc2682cd, 1, True, None)
       

        player_offset = 0x5a4
        character_offset = 0xb48
        p1_c1_health = 0xc268760
        p1_c1_id = 0xc26886c

        for p in range(0, 2):
            for c in range(0, 3):
                self._add_value("p%d_c%d_health" % (p+1, c+1),
                                p1_c1_health + player_offset*p + character_offset*c, 4, True, None)

                self._add_value("p%d_c%d_id" % (p+1, c+1),
                                p1_c1_id + player_offset*p + character_offset*c, 1, True, get_char_name)


