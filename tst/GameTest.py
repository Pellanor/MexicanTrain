import unittest

from src.Domino import Domino
from src.Game import Game


class GameTest(unittest.TestCase):
    def test_deal(self):
        g = Game(5)
        g.deal()
        self.assertEqual(5, len(g.players))
        for player in g.players:
            self.assertEquals(12, len(player.dominoes))
            print("Player ")
            print([str(domino) for domino in player.dominoes])

    def test_start_round(self):
        g = Game(5)
        g.start_round(12)
        for train in g.trains:
            self.assertEqual(12, train.requires)
            self.assertEqual(0, len(train.cars))
            self.assertFalse(train.demand_satisfaction)
        for player in g.players:
            self.assertFalse(player.dominoes.count(Domino(12,12)) > 0)
