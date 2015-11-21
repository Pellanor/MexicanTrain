from collections import namedtuple

from src.Domino import Domino
from src.GameState import GameState
from src.Player import Player
from src.bots.state.BotDomino import BotDomino
from src.bots.state.BotTrain import BotTrain

BotMove = namedtuple('BotMove', ['domino', 'train'])


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
        for domino_id, domino in enumerate(player.dominoes):
            self.draw_domino(domino_id, domino)
        self.played_count = game.played_count

    def draw_domino(self, domino_id: int, domino: Domino):
            bd = BotDomino(domino_id, domino)
            self.dominoes.append(bd)
            self.dominoes_for_number[domino.left].append(bd)
            self.dominoes_for_number[domino.right].append(bd)

    def get_unplayed_count(self, number: int):
        return 13 - self.played_count[number]

    def do_move(self, bot_move: BotMove):
        bot_move.train.requires = bot_move.domino.value.get_other_number(bot_move.train.requires)
        bot_move.train.demands_satisfaction = bot_move.domino.value.is_double

        self.dominoes.remove(bot_move.domino)
        self.dominoes_for_number[bot_move.domino.value.left].remove(bot_move.domino)
        self.dominoes_for_number[bot_move.domino.value.right].remove(bot_move.domino)

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
