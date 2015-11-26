import unittest

from src.Domino import Domino
from src.Player import Player
from src.Train import Train
from src.bots.state.BotTrain import BotTrain
from tst.bots.TestBot import TestBot


class BotTrainTest(unittest.TestCase):
    def test_bot_train(self):
        player_id = 42
        train_id = 9001
        required = 6
        p = Player(player_id, TestBot())
        t = Train(train_id, required, p)
        bt = BotTrain(t, p)
        self.assertTrue(bt.can_add)
        self.assertTrue(bt.am_owner)
        self.assertFalse(bt.identity.mexican)
        self.assertEqual(p, bt.identity.owner)
        self.assertEqual(required, bt.requires)
        bt.cars.append(Domino(2, 3))
        self.assertEqual(0, len(t.cars))

        d1 = Domino(6, 6)
        t.add_domino(d1, p)
        bt = BotTrain(t, p)
        self.assertTrue(bt.demands_satisfaction)
        self.assertEqual(6, bt.requires)
        self.assertEqual(d1, bt.cars.pop())

        d2 = Domino(12, 6)
        t.add_domino(d2, p)
        bt = BotTrain(t, p)
        self.assertFalse(bt.demands_satisfaction)
        self.assertEqual(12, bt.requires)
        self.assertEqual(d2, bt.cars.pop())

    def test_bot_train_cannot_play(self):
        player_id = 42
        owner_id = 24
        train_id = 9001
        required = 6
        p = Player(player_id, TestBot())
        o = Player(owner_id, TestBot())
        t = Train(train_id, required, o)
        bt = BotTrain(t, p)
        self.assertFalse(bt.can_add)
        self.assertFalse(bt.am_owner)
        self.assertFalse(bt.identity.mexican)
        self.assertEqual(o, bt.identity.owner)

    def test_bot_train_public(self):
        player_id = 42
        owner_id = 24
        train_id = 9001
        required = 6
        p = Player(player_id, TestBot())
        o = Player(owner_id, TestBot())
        t = Train(train_id, required, o)
        t.make_public()
        bt = BotTrain(t, p)
        self.assertTrue(bt.can_add)
        self.assertFalse(bt.am_owner)
        self.assertFalse(bt.identity.mexican)
        self.assertEqual(o, bt.identity.owner)

    def test_bot_train_mexican(self):
        player_id = 42
        train_id = 9001
        required = 6
        p = Player(player_id, TestBot())
        t = Train(train_id, required, None)
        bt = BotTrain(t, p)
        self.assertTrue(bt.can_add)
        self.assertFalse(bt.am_owner)
        self.assertTrue(bt.identity.mexican)
        self.assertEqual(None, bt.identity.owner)

    def test_play(self):
        player_id = 42
        train_id = 9001
        required = 6
        p = Player(player_id, TestBot())
        t = Train(train_id, required, p)
        bt = BotTrain(t, p)

        self.assertTrue(bt.play(Domino(3, 6)))
        self.assertEqual(Domino(3, 6), bt.cars[-1])
        self.assertEqual(3, bt.requires)
        self.assertFalse(bt.demands_satisfaction)

        self.assertTrue(bt.play(Domino(3, 3)))
        self.assertEqual(Domino(3, 3), bt.cars[-1])
        self.assertEqual(3, bt.requires)
        self.assertTrue(bt.demands_satisfaction)

        self.assertFalse(bt.play(Domino(6, 6)))
        self.assertEqual(Domino(3, 3), bt.cars[-1])
        self.assertEqual(3, bt.requires)
        self.assertTrue(bt.demands_satisfaction)
