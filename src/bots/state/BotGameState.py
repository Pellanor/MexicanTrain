from collections import namedtuple

from networkx import Graph

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
        left = DominoEdge(domino, domino.left)
        right = DominoEdge(domino, domino.right)
        self.graph.add_edge(left, right, domino=domino)
        for d in self.dominoes:  # type: Domino
            if d.left == domino.left:
                self.graph.add_edge(DominoEdge(d, d.left), left)
            if d.left == domino.right:
                self.graph.add_edge(DominoEdge(d, d.left), right)
            if d.right == domino.right:
                self.graph.add_edge(DominoEdge(d, d.right), right)
            if d.right == domino.left:
                self.graph.add_edge(DominoEdge(d, d.right), left)
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
