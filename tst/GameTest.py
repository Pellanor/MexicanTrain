import unittest

from src.Domino import Domino
from src.Game import Game


class GameTest(unittest.TestCase):
    # def test_deal(self):
    #     g = Game(5)
    #     g.deal()
    #     self.assertEqual(5, len(g.players))
    #     for player in g.players:
    #         self.assertEquals(12, len(player.dominoes))
    #         print("Player ")
    #         print([str(domino) for domino in player.dominoes])
    #
    # def test_start_round(self):
    #     g = Game(5)
    #     g.start_round(12)
    #     for train in g.trains:
    #         self.assertEqual(12, train.requires)
    #         self.assertEqual(0, len(train.cars))
    #         self.assertFalse(train.demand_satisfaction)
    #     for player in g.players:
    #         self.assertFalse(player.dominoes.count(Domino(12,12)) > 0)

    def test_game(self):
        g = Game(5)
        g.play(True)

    def test_game_lots(self):
        players = 5
        games = 1000

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


