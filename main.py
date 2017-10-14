import time
from tourney.marvelvscapcom2 import MarvelVsCapcom2


while 1:
	game = MarvelVsCapcom2()
	game.update()

	for p in range(1,3):
	    print ""
	    print "PLAYER %d" % p
	    for c in range(1,4):
	        print "%s [%f%%]" % (game.__dict__["p%d_c%d_id"%(p,c)], game.__dict__["p%d_c%d_health"%(p,c)]/144.0*100)
	    print ""

	time.sleep(0.2)
