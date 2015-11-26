import itertools
import operator
from collections import namedtuple
from copy import copy
from functools import reduce
from networkx import Graph
from networkx.algorithms.traversal.edgedfs import helper_funcs
from src.Domino import Domino
from src.GameState import GameState
from src.Player import Player
from src.bots.state.BotTrain import BotTrain

BotMove = namedtuple('BotMove', ['domino', 'train'])
DominoEdge = namedtuple('DominoEdge', ['domino', 'value'])


class Path:
    def __init__(self, edge_list):
        self.edge_list = edge_list
        self.edge_set = None
        self.edge_tuple = None

    def get_edge_set(self):
        if self.edge_set is None:
            self.edge_set = set([Path.key(edge) for edge in self.edge_list])
        return self.edge_set

    def get_edge_tuple(self):
        if self.edge_tuple is None:
            self.edge_tuple = tuple([Path.key(edge) for edge in self.edge_list])

    @property
    def size(self):
        return len(self.edge_list)

    @property
    def start(self):
        if self.size > 0:
            return self.edge_list[0][0]
        return None

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.get_edge_tuple() == other.get_edge_tuple()

    def __hash__(self):
        return hash(self.get_edge_tuple())

    def __str__(self):
        return str(self.edge_list)

    # From NetworkX edgedfs.py
    @staticmethod
    def key(edge):
        new_edge = (frozenset(edge[:2]),) + edge[2:]
        return new_edge


class Play:
    def __init__(self, paths):
        self.paths = tuple(paths)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.paths == other.paths

    def __hash__(self):
        return hash(self.paths)

    def __str__(self):
        return str(self.paths)

    @property
    def size(self):
        return sum([path.size for path in self.paths])

    def add_path(self, path: Path):
        self.paths.append(path)

    def add_all(self, paths):
        self.paths.extend(paths)

    def get_paths_from(self, origin: int):
        return [path for path in self.paths if path.start == origin]


class BotGameState:
    def __init__(self, game: GameState, player: Player):
        self.all_trains = []
        self.playable_trains = []
        self.other_trains = []
        self.trains_for_number = {i: [] for i in range(13)}
        self.dominoes_for_number = {i: [] for i in range(13)}
        self.dominoes = []
        for train_id, train in enumerate(game.trains):
            bot_train = BotTrain(train, player)
            if bot_train.am_owner:
                self.my_train = bot_train
            if bot_train.can_add:
                self.playable_trains.append(bot_train)
                self.trains_for_number[bot_train.requires].append(bot_train)
            else:
                self.other_trains.append(bot_train)
            self.all_trains.append(bot_train)
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
        played_on = bot_move.train.requires
        if bot_move.train.play(bot_move.domino):
            self.dominoes.remove(bot_move.domino)
            self.dominoes_for_number[bot_move.domino.left].remove(bot_move.domino)
            self.dominoes_for_number[bot_move.domino.right].remove(bot_move.domino)
            self.played_count[bot_move.domino.left] += 1
            if not bot_move.domino.is_double:
                self.played_count[bot_move.domino.right] += 1

            self.trains_for_number[played_on].remove(bot_move.train)
            self.trains_for_number[bot_move.train.requires].append(bot_move.train)
            return True
        return False

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
        paths.append(Path(edges))
        return paths

    #  Finds all paths through the dominoes graph starting at the specified origin number.
    #  The returned paths will visit each edge no more than once.
    #  Accepts either a single origin number, or a list of origin points.
    #  A list of type Path is returned
    def get_all_paths_from(self, origin):
        nodes = list(self.graph.nbunch_iter(origin))
        if not nodes:
            raise StopIteration

        kwds = {'data': False}
        out_edges, key, tailhead = helper_funcs(self.graph, 'original')

        visited_edges = set()
        paths = {}

        for node in set(nodes):
            paths[node] = []
            for edge in out_edges(node, **kwds):
                edge_key = key(edge)
                if edge_key not in visited_edges:
                    paths[node].extend(self._get_more_edges([], edge, set(), edge_key, kwds, out_edges, key))
        return paths

    def get_longest_paths_from(self, origin):
        long_paths = [Path([])]
        for paths in self.get_all_paths_from(origin).values():
            for path in paths:  # type: Path
                if path.size == long_paths[0].size:
                    long_paths.append(path)
                elif path.size > long_paths[0].size:
                    long_paths = [path]
        return long_paths

    def get_playable_numbers(self):
        return tuple([train.requires for train in self.playable_trains])

    # Returns a set of Plays. A Play being a set of paths with no duplicate edges.
    # This is NP hard, so may raise an AttributeError if the problem space is too big.
    def get_biggest_plays_from(self, origin):
        paths_dict = self.get_all_paths_from(origin)

        for start in paths_dict.keys():
            paths_dict[start].append(Path([]))

        # Because we can have duplicate origin points, we want to allow plays that start with the same number
        # ie. two open trains start with 12, and mexican starts with 5.
        # origin = (5, 12, 12), but path dict is only (5, 12)
        play_list = []
        for k in origin:
            if k in paths_dict:
                play_list.append(paths_dict[k])

        plays = []

        # O(n^len(origin)) aka potentially really really slow, return False if it's too big
        prod = reduce(operator.mul, [len(paths) for paths in play_list], 1)
        if prod > 1000000:
            err_str = "Too many possible plays! {:.2e} - ".format(prod)
            for start_num, size in paths_dict.items():
                err_str += " {}({:n})".format(str(start_num), len(size))
            raise AttributeError(err_str)

        for paths in itertools.product(*play_list):
            unique = True
            for combination in itertools.combinations(paths, 2):
                if not combination[0].get_edge_set().isdisjoint(combination[1].get_edge_set()):
                    unique = False
                    break
            if unique:
                plays.append(Play(paths))

        biggest_plays = []
        biggest_size = 0
        for play in plays:  # type: Play
            size = play.size
            if size == biggest_size:
                biggest_plays.append(play)
            if size > biggest_size:
                biggest_plays = [play]
                biggest_size = size

        return biggest_plays
