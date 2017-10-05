from tourney.marvelvscapcom2 import MarvelVsCapcom2

game = MarvelVsCapcom2()
game.update()

for k in game.__dict__:
    print "%s = %d" % (k, game.k)