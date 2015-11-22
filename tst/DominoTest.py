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
        d3 = Domino(5, 5)
        self.assertEqual(d1, d2)
        self.assertNotEqual(d2, d3)

    def test_hash(self):
        d1 = Domino(2, 3)
        d2 = Domino(2, 3)
        d3 = Domino(5, 5)
        self.assertEqual(hash(d1), hash(d2))
        self.assertNotEqual(hash(d2), hash(d3))

    def test_other(self):
        d = Domino(2,3)
        self.assertEqual(3, d.get_other_number(2))
        self.assertEqual(2, d.get_other_number(3))
        self.assertIsNone(d.get_other_number(42))

    def test_draw(self):
        d = Domino(2, 3)
        self.assertEqual("[2|3]", d.draw(d.left))
        self.assertEqual("[3|2]", d.draw(d.right))
        dd = Domino(6,6)
        self.assertEqual("[ 6 ]", dd.draw(d.right))

    def test_matches(self):
        d1 = Domino(2, 3)
        d2 = Domino(5, 6)
        d3 = Domino(3, 5)
        self.assertFalse(d1.matches(d2))
        self.assertFalse(d2.matches(d1))
        self.assertTrue(d1.matches(d3))
        self.assertTrue(d3.matches(d1))
        self.assertTrue(d2.matches(d3))
        self.assertTrue(d3.matches(d2))


