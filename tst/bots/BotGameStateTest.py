import collections
import unittest

from networkx import edges

from src.Domino import Domino
from src.GameState import GameState
from src.Train import Train
from src.bots.state.BotGameState import BotGameState, BotMove
from src.bots.state.BotTrain import BotTrain
from src.bots.state.Path import Path
from src.bots.state.Play import Play


class BotGameStateTest(unittest.TestCase):
    def get_test_game_state(self):
        game_state = GameState(5)
        player = game_state.players[0]

        game_state.trains.append(Train(0, 10, game_state.players[0]))  # mine
        game_state.trains.append(Train(1, 11, game_state.players[1]))  # private
        game_state.trains.append(Train(2, 12, game_state.players[2]))  # same start as 3
        game_state.trains.append(Train(3, 12, game_state.players[3]))  # same start as 2
        game_state.trains.append(Train(5, 3, None))  # mexican

        game_state.trains[2].make_public()
        game_state.trains[3].make_public()
        game_state.trains[4].make_public()

        player.dominoes.append(Domino(10, 10))  # can play on t0
        player.dominoes.append(Domino(6, 3))  # can play on t4
        player.dominoes.append(Domino(0, 12))  # can play on t2 and t3
        player.dominoes.append(Domino(11, 8))  # cannot play, private
        player.dominoes.append(Domino(4, 3))  # can play on t4
        player.dominoes.append(Domino(2, 12))  # can play on t2 and t3
        player.dominoes.append(Domino(0, 1))  # can play on d2
        player.dominoes.append(Domino(1, 3))  # can play on d4 and d6 and t4
        player.dominoes.append(Domino(3, 0))  # loop between d7 and d8, can also play on d4 and t4

        return game_state, BotGameState(game_state, player)

    def test_bot_game_state(self):
        game_state, bot_game_state = self.get_test_game_state()
        bot_trains = []
        for train in game_state.trains:
            bot_trains.append(BotTrain(train, train.identity.owner))

        self.assertEqual(bot_trains[0], bot_game_state.my_train)
        self.assertIn(bot_trains[1], bot_game_state.other_trains)
        self.assertIn(bot_trains[0], bot_game_state.playable_trains)
        self.assertIn(bot_trains[2], bot_game_state.playable_trains)
        self.assertIn(bot_trains[3], bot_game_state.playable_trains)
        self.assertIn(bot_trains[4], bot_game_state.playable_trains)

        self.assertTrue(bot_game_state.mexican_train.identity.mexican)

        self.assertEqual(game_state.played_count, bot_game_state.played_count)

        for domino in bot_game_state.dominoes:
            self.assertIn(domino, bot_game_state.dominoes_for_number[domino.left])
            self.assertIn(domino, bot_game_state.dominoes_for_number[domino.right])

    def test_draw_domino(self):
        game_state, bot_game_state = self.get_test_game_state()
        d = Domino(3, 3)
        bot_game_state.draw_domino(d)
        self.assertIn(d, bot_game_state.dominoes)
        self.assertIn(BotMove(d, bot_game_state.all_trains[4]), bot_game_state.get_all_valid_moves())
        self.assertIn(d, bot_game_state.dominoes_for_number[3])
        self.assertIn((3, 3), edges(bot_game_state.graph))

    def test_get_unplayed_count(self):
        game_state, bot_game_state = self.get_test_game_state()
        for i in range(0, 13):
            self.assertEqual(13 - game_state.played_count[i], bot_game_state.get_unplayed_count(i))

    def test_do_move(self):
        game_state, bot_game_state = self.get_test_game_state()
        domino = bot_game_state.dominoes[0]
        train = bot_game_state.all_trains[0]
        bot_game_state.do_move(BotMove(domino, train))
        self.assertNotIn(domino, bot_game_state.dominoes)
        self.assertNotIn(domino, bot_game_state.dominoes_for_number[10])
        self.assertEqual(1, bot_game_state.played_count[10])
        self.assertEqual(12, bot_game_state.get_unplayed_count(10))
        self.assertEqual(domino, train.cars[-1])
        self.assertIn(train, bot_game_state.trains_for_number[10])

        domino = bot_game_state.dominoes[0]  # Domino(6, 3) was previously [1], but is now []0 since we popped [0]
        train = bot_game_state.all_trains[4]
        bot_game_state.do_move(BotMove(domino, train))
        self.assertNotIn(domino, bot_game_state.dominoes)
        self.assertNotIn(domino, bot_game_state.dominoes_for_number[6])
        self.assertNotIn(domino, bot_game_state.dominoes_for_number[3])
        self.assertEqual(1, bot_game_state.played_count[6])
        self.assertEqual(1, bot_game_state.played_count[3])
        self.assertEqual(12, bot_game_state.get_unplayed_count(6))
        self.assertEqual(12, bot_game_state.get_unplayed_count(3))
        self.assertEqual(domino, train.cars[-1])
        self.assertIn(train, bot_game_state.trains_for_number[6])
        self.assertNotIn(train, bot_game_state.trains_for_number[3])

    def test_get_all_valid_moves(self):
        game_state, bot_game_state = self.get_test_game_state()

        moves = bot_game_state.get_all_valid_moves()

        expected_moves = [BotMove(bot_game_state.dominoes[0], bot_game_state.all_trains[0]),
                          BotMove(bot_game_state.dominoes[1], bot_game_state.all_trains[4]),
                          BotMove(bot_game_state.dominoes[2], bot_game_state.all_trains[2]),
                          BotMove(bot_game_state.dominoes[2], bot_game_state.all_trains[3]),
                          BotMove(bot_game_state.dominoes[4], bot_game_state.all_trains[4]),
                          BotMove(bot_game_state.dominoes[5], bot_game_state.all_trains[3]),
                          BotMove(bot_game_state.dominoes[5], bot_game_state.all_trains[2]),
                          BotMove(bot_game_state.dominoes[7], bot_game_state.all_trains[4]),
                          BotMove(bot_game_state.dominoes[8], bot_game_state.all_trains[4])]
        self.assertEqual(collections.Counter(expected_moves), collections.Counter(moves))

    def test_get_all_paths_from(self):
        game_state, bot_game_state = self.get_test_game_state()

        path_dict = bot_game_state.get_all_paths_from(12)
        self.assertEqual(1, len(path_dict))
        paths = path_dict[12]

        expected_paths = [Path([(12, 2)]),
                          Path([(12, 0)]),
                          Path([(12, 0), (0, 1)]),
                          Path([(12, 0), (0, 1), (1, 3)]),
                          Path([(12, 0), (0, 1), (1, 3), (3, 4)]),
                          Path([(12, 0), (0, 1), (1, 3), (3, 6)]),
                          Path([(12, 0), (0, 1), (1, 3), (3, 0)]),
                          Path([(12, 0), (0, 3)]),
                          Path([(12, 0), (0, 3), (3, 4)]),
                          Path([(12, 0), (0, 3), (3, 6)]),
                          Path([(12, 0), (0, 3), (3, 1)]),
                          Path([(12, 0), (0, 3), (3, 1), (1, 0)])]
        self.assertEqual(collections.Counter(expected_paths), collections.Counter(paths))

        path_dict = bot_game_state.get_all_paths_from(3)
        self.assertEqual(1, len(path_dict))
        paths = path_dict[3]

        expected_paths = [Path([(3, 4)]),
                          Path([(3, 6)]),
                          Path([(3, 0)]),
                          Path([(3, 1)]),
                          Path([(3, 1), (1, 0)]),
                          Path([(3, 1), (1, 0), (0, 12)]),
                          Path([(3, 1), (1, 0), (0, 12), (12, 2)]),
                          Path([(3, 1), (1, 0), (0, 3)]),
                          Path([(3, 1), (1, 0), (0, 3), (3, 4)]),
                          Path([(3, 1), (1, 0), (0, 3), (3, 6)]),
                          Path([(3, 0), (0, 12)]),
                          Path([(3, 0), (0, 12), (12, 2)]),
                          Path([(3, 0), (0, 1)]),
                          Path([(3, 0), (0, 1), (1, 3)]),
                          Path([(3, 0), (0, 1), (1, 3), (3, 4)]),
                          Path([(3, 0), (0, 1), (1, 3), (3, 6)])]
        self.assertEqual(collections.Counter(expected_paths), collections.Counter(paths))

    def test_get_longest_paths_from(self):
        game_state, bot_game_state = self.get_test_game_state()

        paths = bot_game_state.get_longest_paths_from(bot_game_state.get_playable_numbers())
        expected_paths = [Path([(12, 0), (0, 1), (1, 3), (3, 4)]),
                          Path([(12, 0), (0, 1), (1, 3), (3, 6)]),
                          Path([(12, 0), (0, 1), (1, 3), (3, 0)]),
                          Path([(12, 0), (0, 3), (3, 1), (1, 0)]),
                          Path([(3, 1), (1, 0), (0, 12), (12, 2)]),
                          Path([(3, 1), (1, 0), (0, 3), (3, 4)]),
                          Path([(3, 1), (1, 0), (0, 3), (3, 6)]),
                          Path([(3, 0), (0, 1), (1, 3), (3, 4)]),
                          Path([(3, 0), (0, 1), (1, 3), (3, 6)])]
        self.assertEqual(collections.Counter(expected_paths), collections.Counter(paths))

    def test_get_playable_numbers(self):
        game_state, bot_game_state = self.get_test_game_state()
        playable_numbers = bot_game_state.get_playable_numbers()
        self.assertEqual(collections.Counter(playable_numbers), collections.Counter([3, 10, 12, 12]))

    def test_get_biggest_plays_from(self):
        game_state, bot_game_state = self.get_test_game_state()

        plays = bot_game_state.get_biggest_plays_from(bot_game_state.get_playable_numbers())
        expected_play = Play([Path([(10, 10)]),
                              Path([(12, 2)]),
                              Path([(3, 4)]),
                              Path([(12, 0), (0, 1), (1, 3), (3, 0)])])

        self.assertEqual(28, len(plays))
        self.assertIn(expected_play, plays)
