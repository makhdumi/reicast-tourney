import time
from tourney.marvelvscapcom2 import MarvelVsCapcom2


game = MarvelVsCapcom2()
while 1:
	game.update()
	game.next_state()
	print("game state = %d" % game.state)

	time.sleep(0.5)
