import unittest

from src.Domino import Domino
from src.Game import Game
from src.bots.BotGameState import BotGameState


class TestBotGameState(unittest.TestCase):
    def test_get_unplayed_count(self):
        g = Game(5)
        p = g.players[0]
        state = BotGameState(g, p)
        self.assertEqual(13, state.get_unplayed_count(0))
        g.start_round(12)
        self.assertEqual(12, state.get_unplayed_count(12))
        g.trains[5].add_domino(Domino(12, 11), p)
        self.assertEqual(11, state.get_unplayed_count(12))

    def test_get_all_train_ends(self):
        g = Game(5)
        p = g.players[0]
        state = BotGameState(g, p)
        g.start_round(12)
        print([str(train_end) for train_end in state.get_all_trains_ends()])

    def test_get_playable_train_ends(self):
        g = Game(5)
        p = g.players[0]
        state = BotGameState(g, p)
        g.start_round(12)
        print([str(train_end) for train_end in state.get_playable_train_ends()])
