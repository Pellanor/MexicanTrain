from copy import copy
from random import shuffle

from src.Domino import make_domino_from_edge
from src.bots.BaseBot import BaseBot
from src.bots.state.BotGameState import BotGameState, BotMove


class FatBot(BaseBot):

    first_turn_moves = None
    played = []
    initial = []

    def get_move(self, game_state: BotGameState):
        if self.turn == 0:
            if self.first_turn_moves is None:
                self.initial = copy(game_state.dominoes)
                try:
                    plays = game_state.get_biggest_plays(game_state.get_playable_numbers())
                    shuffle(plays)
                    play = plays.pop()
                    self.first_turn_moves = []
                    used_trains = []
                    for path in play:
                        if path.size > 0:
                            trains = game_state.trains_for_number[path.start]
                            shuffle(trains)
                            used_trains.append(trains[0])
                            self.first_turn_moves.extend(
                                [BotMove(make_domino_from_edge(edge), trains[0]) for edge in path.edge_list])
                except AttributeError as e:
                    print(e)
                    paths = game_state.get_longest_paths_from(game_state.get_playable_numbers())
                    shuffle(paths)
                    path = paths.pop()
                    trains = game_state.trains_for_number[path.start]
                    shuffle(trains)
                    self.first_turn_moves = [BotMove(make_domino_from_edge(edge), trains[0]) for edge in path.edge_list]
            if len(self.first_turn_moves) > 0:
                move = self.first_turn_moves.pop(0)
                self.played.append(move)
                return move
        possible_moves = game_state.get_all_valid_moves()
        if len(possible_moves) > 0:
            shuffle(possible_moves)
            return possible_moves.pop()
        return None

    def new_round(self, round_number: int):
        super(FatBot, self).new_round(round_number)
        self.first_turn_moves = None
        self.played = []
        self.initial = []
