from src.bots.BaseBot import BaseBot
from src.bots.state.BotGameState import BotGameState, BotMove
from src.bots.strategy.Random import Random


class FatBot(BaseBot):
    first_turn_moves = []

    def __init__(self, strategy=Random()):
        super().__init__()
        self.strategy = strategy

    def get_move(self, game_state: BotGameState):
        try:
            if self.turn == 0:
                if len(self.first_turn_moves) == 0:
                    self.first_turn_moves = self.get_move_list_for_biggest_play_from(game_state.get_playable_numbers(),
                                                                                     game_state, self.strategy)
                if len(self.first_turn_moves) > 0:
                    move = self.first_turn_moves.pop(0)
                    asd = move.train.identity
                    return move
            move = self.get_valid_move(game_state, self.strategy)
            asd = move.train.identity
            return move
        except AttributeError as ae:
            print(ae)


    def report_invalid_move(self, move: BotMove):
        super(FatBot, self).report_invalid_move(move)
        self.first_turn_moves = []

    def new_round(self, round_number: int):
        super(FatBot, self).new_round(round_number)
        self.first_turn_moves = []
