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
from src.bots.state.BotPlayer import BotPlayer
from src.bots.state.BotTrain import BotTrain
from src.bots.state.Path import Path
from src.bots.state.Play import Play

BotMove = namedtuple('BotMove', ['domino', 'train'])


class BotGameState:
    """
    The BotGameState is the main method for a bot and game to communicate with each other.
    The BotGameState will not allow the bot to manipulate any aspects of the game state.
    The Game will include an up to date version of the BotGameState in each of its calls to the Bot.
    """

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
        self.played_count = copy(game.played_count)
        self.players = [BotPlayer(train.identity.owner, train, train.identity.owner == player) for train in game.trains
                        if not train.identity.mexican]

    @property
    def mexican_train(self) -> BotTrain:
        """
        Gets the Mexican Train, that anybody can play on
        :return: a BotTrain for the mexican train
        """
        return self.all_trains[-1]

    def draw_domino(self, domino: Domino):
        """
        Draws the specified domino, adding it to all internal data structures.
        :param domino: The domino to add
        """
        self.graph.add_edge(domino.left, domino.right)
        self.dominoes.append(domino)
        self.dominoes_for_number[domino.left].append(domino)
        self.dominoes_for_number[domino.right].append(domino)

    def get_unplayed_count(self, number: int) -> int:
        """
        Returns a count of the dominoes that have not yet been played containing the specified number.
        :param number: the expected number
        :return: a count of the dominoes containing the given number
        """
        return 13 - self.played_count[number]

    def do_move(self, bot_move: BotMove) -> bool:
        """
        Executes the specified move in the current bot state.
        This is to be called by the game when it runs a move for the bot to update the bot state.
        This should not be called by the bot, at risk of desynchronising the bot state from the actual game state
        :param bot_move: The move to make
        :return: a boolean indicating if the move was applied successfully
        """
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
        """
        Checks the current bot state for all legal moves, and returns a list of them
        :return: A list of BotMove
        """
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

    def _get_more_edges(self, in_edges, new_edge, in_visited_edges, new_key, kwds, out_edges, key):
        """
        recursive helper function for get_all_paths_from
        :param in_edges: incoming edges, aka dominoes already in the chain
        :param new_edge: the edge to add, aka the latest domino
        :param in_visited_edges: set of keys for the dominoes already in the chain
        :param new_key: the key for the edge to be added
        :param kwds: used by NetworkX for things
        :param out_edges: All remaining dominoes
        :param key: the key function
        :return: a Path list where each path starts with in_edges and continues to all possible outcomes
        """
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

    def get_all_paths_from(self, origin):
        """
        Finds all paths through the dominoes graph starting at the specified origin number.
        The returned paths will visit each edge (aka domino) no more than once.
        :param origin: The number to start on, or an iterable containing start numbers.
            All paths will start with that number.
        :return: A Path list for all possible paths.
        """
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
        """
        Find all paths through the domino graph starting at the specified origin number which have the greatest length.
        The returned paths will visit each edge (aka domino) no more than once.
        :param origin: The number to start on, or an iterable containing start numbers.
            All paths will start with one of those number.
        :return: A Path list for all possible paths of greatest length.
        """
        long_paths = [Path([])]
        for paths in self.get_all_paths_from(origin).values():
            for path in paths:
                if path.size == long_paths[0].size:
                    long_paths.append(path)
                elif path.size > long_paths[0].size:
                    long_paths = [path]
        return long_paths

    def get_playable_numbers(self):
        return tuple([train.requires for train in self.playable_trains])

    def get_biggest_plays_from(self, origin):
        """
        Finds all Plays which have the greatest length, starting from the specified origin.
        A Play is a set of paths sharing no dominoes between them.
        This is NP hard, so may raise an AttributeError if the problem space is too big.
        :param origin: The number to start on, or an iterable containing start numbers.
            All paths will start with one of those number.
        :return: A Play List for all possible plays of greatest length
        """
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
                play = Play(paths)
                # It's not a valid play if we have multiple unsatisfied doubles.
                # There will be other plays that drop those.
                if not play.satisfaction_count > 1:
                    plays.append(Play(paths))

        biggest_plays = []
        biggest_size = 0
        for play in plays:
            size = play.size
            if size == biggest_size:
                biggest_plays.append(play)
            if size > biggest_size:
                biggest_plays = [play]
                biggest_size = size

        return biggest_plays
