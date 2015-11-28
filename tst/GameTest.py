import unittest

from src.Game import Game


class GameTest(unittest.TestCase):

    def test_game(self):
        g = Game(5)
        g.play(True)

    def test_game_lots(self):
        players = 5
        games = 100

        stats = {i: [0, 0] for i in range(players)}
        for count in range(games):
            g = Game(players)
            g.play()
            for i, s in g.get_stats().items():
                stats[i][0] += s[0]
                stats[i][1] += s[1]
        for i, s in stats.items():
            print("Player {} - Victories {} ({}%), Score {}".
                  format(i, str(s[0]), str((s[0]*100) / (games*13)), str(s[1])))


