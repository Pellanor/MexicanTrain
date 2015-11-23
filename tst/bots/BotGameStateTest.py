import unittest

from networkx import all_simple_paths, info, edges, nodes, edge_dfs
from src.Domino import Domino, make_domino_from_edge
from src.GameState import GameState
from src.Player import Player
from src.Train import Train
from src.bots.state.BotGameState import BotGameState, BotMove, DominoEdge
from src.bots.state.BotTrain import BotTrain
from src.bots.state.BotPlayer import BotPlayer
from tst.bots.TestBot import TestBot


class BotGameStateTest(unittest.TestCase):
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

    def test_bot_game_state(self):
        game_state = GameState(5)
        player = game_state.players[0]

        game_state.trains.append(Train(0, 10, game_state.players[0]))
        game_state.trains.append(Train(1, 11, game_state.players[1]))
        game_state.trains.append(Train(2, 12, game_state.players[2]))
        game_state.trains.append(Train(3, 5, game_state.players[3]))
        game_state.trains.append(Train(4, 4, game_state.players[4]))
        game_state.trains.append(Train(5, 3, None))

        game_state.trains[2].make_public()
        game_state.trains[3].make_public()
        game_state.trains[4].make_public()
        game_state.trains[5].make_public()

        player.dominoes.append(Domino(10, 10))  # can play on t0
        player.dominoes.append(Domino(6, 4))  # can play on t4
        player.dominoes.append(Domino(0, 1))
        player.dominoes.append(Domino(0, 12))  # can play on t2
        player.dominoes.append(Domino(11, 8))
        player.dominoes.append(Domino(11, 7))
        player.dominoes.append(Domino(4, 3))  # can play on t4 and t5
        player.dominoes.append(Domino(2, 12))  # can play on t2

        bgs = BotGameState(game_state, player)
        bot_trains = []
        for train in game_state.trains:
            bot_trains.append(BotTrain(train, train.identity.owner))

        self.assertEqual(bot_trains[0], bgs.my_train)
        self.assertIn(bot_trains[1], bgs.other_trains)
        self.assertIn(bot_trains[0], bgs.playable_trains)
        self.assertIn(bot_trains[2], bgs.playable_trains)
        self.assertIn(bot_trains[3], bgs.playable_trains)
        self.assertIn(bot_trains[4], bgs.playable_trains)
        self.assertIn(bot_trains[5], bgs.playable_trains)

        moves = bgs.get_all_valid_moves()
        self.assertEqual(6, len(moves))
        self.assertIn(BotMove(bgs.dominoes[0], bot_trains[0]), moves)
        self.assertIn(BotMove(bgs.dominoes[1], bot_trains[4]), moves)
        self.assertIn(BotMove(bgs.dominoes[3], bot_trains[2]), moves)
        self.assertIn(BotMove(bgs.dominoes[6], bot_trains[4]), moves)
        self.assertIn(BotMove(bgs.dominoes[6], bot_trains[4]), moves)
        self.assertIn(BotMove(bgs.dominoes[7], bot_trains[2]), moves)

        self.assertEqual(game_state.played_count, bgs.played_count)

    def test_graph(self):
        game_state = GameState(5)
        for train_id, player in enumerate(game_state.players):
            game_state.trains.append(Train(train_id, 12, player))
        game_state.trains.append(Train(len(game_state.trains), 5, None))
        player = game_state.players[0]
        player.dominoes = [Domino(12, 3), Domino(3, 9), Domino(9, 7), Domino(7, 0), Domino(0, 10), Domino(10, 8),
                           Domino(10, 10), Domino(10, 5), Domino(5, 3), Domino(5, 4), Domino(5, 6), Domino(6, 7)]

        bgs = BotGameState(game_state, player)
        print(*nodes(bgs.graph), sep='\n')
        print(*edges(bgs.graph), sep='\n')

        print('\n')

        # for origin, paths in bgs.get_all_paths_from(bgs.get_playable_numbers()).items():
        #     print("Origin: " + str(origin))
        #     for path in paths:
        #         print(path)
        for path in bgs.get_longest_paths_from(bgs.get_playable_numbers()):
            print(path)
        print('\n')
        for play in bgs.get_biggest_plays(bgs.get_playable_numbers()):
            print("Play: ")
            for path in play:
                print(path)
