from collections import namedtuple
from copy import copy

import itertools
from networkx import Graph, all_simple_paths, edge_dfs
from networkx.algorithms.traversal.edgedfs import helper_funcs

from src.Domino import Domino
from src.GameState import GameState
from src.Player import Player
from src.bots.state.BotTrain import BotTrain

BotMove = namedtuple('BotMove', ['domino', 'train'])
DominoEdge = namedtuple('DominoEdge', ['domino', 'value'])


class BotGameState:
    def __init__(self, game: GameState, player: Player):
        self.all_trains = []
        self.playable_trains = []
        self.other_trains = []
        for train_id, train in enumerate(game.trains):
            bot_train = BotTrain(train, player)
            if bot_train.am_owner:
                self.my_train = bot_train
            if bot_train.can_add:
                self.playable_trains.append(bot_train)
            else:
                self.other_trains.append(bot_train)
            self.all_trains.append(bot_train)
        self.dominoes_for_number = {i: [] for i in range(13)}
        self.dominoes = []
        self.graph = Graph()
        for domino in player.dominoes:
            self.draw_domino(domino)
        self.played_count = game.played_count

    def draw_domino(self, domino: Domino):
        self.graph.add_edge(domino.left, domino.right)
        self.dominoes.append(domino)
        self.dominoes_for_number[domino.left].append(domino)
        self.dominoes_for_number[domino.right].append(domino)

    def get_unplayed_count(self, number: int) -> int:
        return 13 - self.played_count[number]

    def do_move(self, bot_move: BotMove):
        bot_move.train.requires = bot_move.domino.get_other_number(bot_move.train.requires)
        bot_move.train.demands_satisfaction = bot_move.domino.is_double

        self.dominoes.remove(bot_move.domino)
        self.dominoes_for_number[bot_move.domino.left].remove(bot_move.domino)
        self.dominoes_for_number[bot_move.domino.right].remove(bot_move.domino)

    def get_all_valid_moves(self):
        valid_moves = set()
        # Check if any train demands satisfaction
        for bot_train in self.playable_trains:
            if bot_train.demands_satisfaction:
                for bot_domino in self.dominoes_for_number[bot_train.requires]:
                    valid_moves.add(BotMove(bot_domino, bot_train))
                # Only one train can demand satisfaction at a time, no other moves are possible
                return list(valid_moves)
        # Satisfaction not required. Add all possible moves.
        for bot_train in self.playable_trains:
            for bot_domino in self.dominoes_for_number[bot_train.requires]:
                valid_moves.add(BotMove(bot_domino, bot_train))
        return list(valid_moves)

    #  recursive helper function for get_all_paths_from
    def _get_more_edges(self, in_edges, new_edge, in_visited_edges, new_key, kwds, out_edges, key):
        edges = copy(in_edges)
        visited_edges = copy(in_visited_edges)
        edges.append(new_edge)
        visited_edges.add(new_key)
        node = new_edge[1]

        paths = []
        for edge in out_edges(node, **kwds):
            edge_key = key(edge)
            if edge_key not in visited_edges:
                paths.extend(self._get_more_edges(edges, edge, visited_edges, edge_key, kwds, out_edges, key))
        paths.append(edges)
        return paths

    #  Finds all paths through the dominoes graph starting at the specified origin number.
    #  The returned paths will visit each edge no more than once.
    #  Accepts either a single origin number, or a list of origin points.
    def get_all_paths_from(self, origin):
        nodes = list(self.graph.nbunch_iter(origin))
        if not nodes:
            raise StopIteration

        kwds = {'data': False}
        out_edges, key, tailhead = helper_funcs(self.graph, 'original')

        visited_edges = set()
        paths = {}

        for node in nodes:
            paths[node] = []
            for edge in out_edges(node, **kwds):
                edge_key = key(edge)
                if edge_key not in visited_edges:
                    paths[node].extend(self._get_more_edges([], edge, set(), edge_key, kwds, out_edges, key))
        return paths

    def get_longest_paths_from(self, origin):
        long_paths = [[]]
        for paths in self.get_all_paths_from(origin).values():
            for path in paths:
                if len(path) == len(long_paths[0]):
                    long_paths.append(path)
                elif len(path) > len(long_paths[0]):
                    long_paths = [path]
        return long_paths

    def get_playable_numbers(self):
        numbs = set()
        for train in self.playable_trains:
            numbs.add(train.requires)
        return numbs

    def get_biggest_plays(self, origin):
        paths_dict = self.get_all_paths_from(origin)
        out_edges, key, tailhead = helper_funcs(self.graph, 'original')

        path_sets_dict = {}
        path_map = dict()
        plays = set()
        for head, paths in paths_dict.items():
            #  Start with an empty set so we're not forced to use bot origins
            path_sets_dict[head] = [frozenset()]
            for path in paths:
                path_set = frozenset([key(edge) for edge in path])
                path_sets_dict[head].append(path_set)
                path_map[path_set] = path

        for path_sets in itertools.product(*path_sets_dict.values()):
            unique = True
            for combination in itertools.combinations(path_sets, 2):
                if not combination[0].isdisjoint(combination[1]):
                    unique = False
                    break
            if unique:
                plays.add(path_sets)

        biggest_plays = set(set(set()))
        biggest_size = 0
        for play in plays:
            size = 0
            for path_set in play:
                size += len(path_set)
            if size == biggest_size:
                biggest_plays.add(play)
            if size > biggest_size:
                biggest_plays = {play}
                biggest_size = size

        val = []
        for play in biggest_plays:
            val.append([])
            for path_set in play:
                val[-1].append(path_map[path_set])
        return val
