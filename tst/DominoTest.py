import unittest

from src.Domino import Domino


class DominoTest(unittest.TestCase):

    def test_construction(self):
        d = Domino(2, 3)
        self.assertEqual(2, d.left)
        self.assertEqual(3, d.right)

    def test_equals(self):
        d1 = Domino(2, 3)
        d2 = Domino(2, 3)
        self.assertEqual(d1, d2)

