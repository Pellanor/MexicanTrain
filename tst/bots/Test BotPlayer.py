import unittest

from src.Domino import Domino
from src.Player import Player
from src.Train import Train
from src.bots.state.BotPlayer import BotPlayer
from src.bots.state.BotTrain import BotTrain
from tst.bots.TestBot import TestBot


class TestBotPlayer(unittest.TestCase):

    def test_bot_player(self):
        player_id = 42
        p = Player(player_id, TestBot())
        p.dominoes.append(Domino(2, 3))
        train_id = 9001
        required = 6
        t = Train(train_id, required, p)
        bt = BotTrain(t, p)
        bp = BotPlayer(p, bt)
        self.assertEqual(player_id, bp.player_id)
        self.assertEqual(len(p.dominoes), bp.tile_count)
        self.assertEqual(bt, bp.train)
