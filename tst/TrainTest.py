import unittest

from src.Domino import Domino
from src.Player import Player
from src.Train import Train


class TrainTest(unittest.TestCase):
    def test_demands_satisfaction(self):
        t = Train(5, 5, Player(5))
        d = Domino(5, 5)
        t.add_domino(d, Player(5))
        self.assertTrue(t.demand_satisfaction)

    def test_does_not_demand_satisfaction(self):
        t = Train(2, 2, Player(2))
        d = Domino(2, 3)
        t.add_domino(d, Player(2))
        self.assertFalse(t.demand_satisfaction)

    def test_can_add_domino(self):
        t = Train(2, 2, Player(2))
        d = Domino(2, 3)
        self.assertTrue(t.add_domino(d, Player(2)))

    def test_cannot_add_domino(self):
        t = Train(5, 5, Player(5))
        d = Domino(2, 3)
        self.assertFalse(t.add_domino(d, Player(2)))

    def test_private_train(self):
        t = Train(2, 2, Player(2))
        t.make_private()
        d = Domino(2, 3)
        self.assertTrue(t.add_domino(d, Player(2)))
        self.assertFalse(t.add_domino(d, Player(1)))

    def test_private_to_public(self):
        t = Train(2, 2, Player(2))
        t.make_private()
        t.make_public()
        d = Domino(2, 3)
        self.assertTrue(t.add_domino(d, Player(2)))

    def test_update_required(self):
        t = Train(2, 2, Player(2))
        d = Domino(2, 3)
        t.add_domino(d, Player(2))
        self.assertEqual(3, t.requires)
