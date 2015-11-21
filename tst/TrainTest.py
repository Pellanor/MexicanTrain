import unittest

from src.Domino import Domino
from src.Player import Player
from src.Train import Train
from tst.bots.TestBot import TestBot


class TrainTest(unittest.TestCase):
    player_two = Player(2, TestBot())
    player_five = Player(5, TestBot())

    def test_mexican(self):
        t1 = Train(1, 1, None)
        self.assertTrue(t1.identity.mexican)
        self.assertFalse(t1.private)

        t2 = Train(2, 2, self.player_two)
        self.assertFalse(t2.identity.mexican)
        self.assertTrue(t2.private)

    def test_demands_satisfaction(self):
        t = Train(5, 5, self.player_five)
        d = Domino(5, 5)
        t.add_domino(d, self.player_five)
        self.assertTrue(t.demands_satisfaction)
        self.assertFalse(t.private)

    def test_does_not_demand_satisfaction(self):
        t = Train(2, 2, self.player_two)
        d = Domino(2, 3)
        t.add_domino(d, self.player_two)
        self.assertFalse(t.demands_satisfaction)
        self.assertTrue(t.private)

    def test_provide_satisfaction(self):
        t = Train(5, 5, self.player_five)
        d = Domino(5, 5)
        t.add_domino(d, self.player_five)
        self.assertTrue(t.demands_satisfaction)
        self.assertFalse(t.private)
        t.add_domino(Domino(3, 5), self.player_five)
        self.assertFalse(t.demands_satisfaction)
        self.assertTrue(t.private)

    def test_can_add_domino(self):
        t = Train(2, 2, self.player_two)
        d = Domino(2, 3)
        self.assertTrue(t.add_domino(d, self.player_two))

    def test_cannot_add_domino(self):
        t = Train(5, 5, self.player_five)
        d = Domino(2, 3)
        self.assertFalse(t.add_domino(d, self.player_two))

    def test_private_train(self):
        t = Train(2, 2, self.player_two)
        t.make_private()
        d = Domino(2, 3)
        self.assertTrue(t.add_domino(d, self.player_two))
        self.assertFalse(t.add_domino(d, Player(1, TestBot())))

    def test_private_to_public(self):
        t = Train(2, 2, self.player_two)
        t.make_private()
        t.make_public()
        d = Domino(2, 3)
        self.assertTrue(t.add_domino(d, self.player_two))

    def test_update_required(self):
        t = Train(2, 2, self.player_two)
        d = Domino(2, 3)
        t.add_domino(d, self.player_two)
        self.assertEqual(3, t.requires)
