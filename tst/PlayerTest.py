import unittest

from src.Domino import Domino
from src.Player import Player
from tst.bots.TestBot import TestBot


class PlayerTest(unittest.TestCase):
    def test_equals(self):
        p1 = Player(1, TestBot())
        p2 = Player(1, TestBot())
        p3 = Player(3, TestBot())

        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)

    def test_give_domino(self):
        p = Player(1, TestBot())
        d = Domino(2, 3)
        p.give_domino(d)
        self.assertTrue(p.dominoes.__contains__(d))
