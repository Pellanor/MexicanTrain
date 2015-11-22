import unittest

from src.Domino import Domino
from src.bots.state.BotDomino import BotDomino


class BotDominoTest(unittest.TestCase):

    def test_add_no_match(self):
        bd = BotDomino(Domino(3, 5))
        bd.add_domino(BotDomino(Domino(2, 2)))
        self.assertEqual(0, len(bd.left))
        self.assertEqual(0, len(bd.right))

    def test_add_left(self):
        bd = BotDomino(Domino(3, 5))
        bd2 = BotDomino(Domino(3, 2))
        bd.add_domino(bd2)
        self.assertEqual(1, len(bd.left))
        self.assertEqual(0, len(bd.right))
        self.assertEqual(bd2, bd.left[0])

    def test_add_right(self):
        bd = BotDomino(Domino(3, 5))
        bd2 = BotDomino(Domino(5, 2))
        bd.add_domino(bd2)
        self.assertEqual(0, len(bd.left))
        self.assertEqual(1, len(bd.right))
        self.assertEqual(bd2, bd.right[0])

    def test_double_add(self):
        bd = BotDomino(Domino(5, 5))
        bd2 = BotDomino(Domino(2, 5))
        bd.add_domino(bd2)
        self.assertEqual(1, len(bd.left))
        self.assertEqual(1, len(bd.right))
        self.assertEqual(bd2, bd.left[0])
        self.assertEqual(bd2, bd.right[0])

    def test_add_all(self):
        bd = BotDomino(Domino(3, 5))
        dominoes = [BotDomino(Domino(2, 2)), BotDomino(Domino(2, 5)), BotDomino(Domino(3, 2)), BotDomino(Domino(5, 5))]
        bd.add_all(dominoes)
        self.assertEqual(1, len(bd.left))
        self.assertEqual(2, len(bd.right))
        self.assertEqual(dominoes[2], bd.left[0])
        self.assertEqual(dominoes[1], bd.right[0])
        self.assertEqual(dominoes[3], bd.right[1])

    def test_remove(self):
        bd = BotDomino(Domino(3, 5))
        bd2 = BotDomino(Domino(3, 2))
        bd.add_domino(bd2)
        bd.remove_domino(bd2)
        self.assertEqual(0, len(bd.left))
        self.assertEqual(0, len(bd.right))

    def test_play(self):
        bd = BotDomino(Domino(3, 5))
        dominoes = [BotDomino(Domino(2, 2)), BotDomino(Domino(2, 5)), BotDomino(Domino(3, 2)), BotDomino(Domino(5, 5))]
        bd.add_all(dominoes)
        for bot_domino in dominoes:
            bot_domino.add_domino(bd)
        self.assertEqual(0, dominoes[0].left.count(bd))
        self.assertEqual(0, dominoes[0].right.count(bd))
        self.assertEqual(0, dominoes[1].left.count(bd))
        self.assertEqual(1, dominoes[1].right.count(bd))
        self.assertEqual(1, dominoes[2].left.count(bd))
        self.assertEqual(0, dominoes[2].right.count(bd))
        self.assertEqual(1, dominoes[3].left.count(bd))
        self.assertEqual(1, dominoes[3].right.count(bd))
        bd.play()
        for bot_domino in dominoes:
            self.assertEqual(0, bot_domino.left.count(bd))
            self.assertEqual(0, bot_domino.right.count(bd))
