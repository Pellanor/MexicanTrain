import unittest

from src.Domino import Domino
from src.GameState import GameState
from src.Player import Player
from src.Train import Train
from tst.bots.TestBot import TestBot


class GameStateTest(unittest.TestCase):
    def test_draw_domino(self):
        game_state = GameState(1)
        domino = Domino(2, 3)
        game_state.dominoes.append(domino)
        player = Player(0, TestBot())
        self.assertTrue(game_state.draw_domino(player))
        self.assertEqual(1, len(player.dominoes))
        self.assertEqual(domino, player.dominoes.pop())

    def test_draw_domino_none_to_draw(self):
        game_state = GameState(1)
        player = Player(0, TestBot())
        self.assertFalse(game_state.draw_domino(player))
        self.assertEqual(0, len(player.dominoes))

    def test_draw_and_check_no_match(self):
        game_state = GameState(1)
        domino = Domino(2, 3)
        game_state.dominoes.append(domino)
        player = Player(0, TestBot())
        self.assertFalse(game_state.draw_domino_and_check_for_start(player, Domino(12, 12)))
        self.assertEqual(1, len(player.dominoes))
        self.assertEqual(domino, player.dominoes.pop())

    def test_draw_and_check_match(self):
        game_state = GameState(1)
        # This is the next tile that the player will draw after drawing and placing the starting tile
        domino = Domino(2, 3)
        game_state.dominoes.append(domino)
        game_state.dominoes.append(Domino(12, 12))
        player = Player(0, TestBot())
        self.assertTrue(game_state.draw_domino_and_check_for_start(player, Domino(12, 12)))
        self.assertEqual(1, len(player.dominoes))
        self.assertEqual(domino, player.dominoes.pop())

    def test_draw_and_check_match_last_tile(self):
        game_state = GameState(1)
        game_state.dominoes.append(Domino(12, 12))
        player = Player(0, TestBot())
        self.assertTrue(game_state.draw_domino_and_check_for_start(player, Domino(12, 12)))
        self.assertEqual(0, len(player.dominoes))

    def test_draw_and_check_none_to_draw(self):
        game_state = GameState(1)
        player = Player(0, TestBot())
        # Need to use a lambda here or the test just fails with the RuntimeError
        self.assertRaises(RuntimeError, lambda: game_state.draw_domino_and_check_for_start(player, Domino(12, 12)))
        self.assertEqual(0, len(player.dominoes))

    # The bulk of the logic for the legality of the placement is in the Train class. It is not tested here.
    def test_place_domino(self):
        game_state = GameState(1)
        player = Player(0, TestBot())
        domino = Domino(2, 3)
        player.dominoes.append(domino)
        train = Train(0, 2, player)
        game_state.place_domino(train, domino, player)
        self.assertEqual(0, len(player.dominoes))
        self.assertEqual(domino, game_state.played.pop())
        self.assertEqual(1, game_state.played_count[2])
        self.assertEqual(1, game_state.played_count[3])
        self.assertEqual(0, game_state.played_count[0])




