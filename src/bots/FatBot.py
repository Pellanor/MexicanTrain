from src.bots.BaseBot import BaseBot
from src.bots.state.BotGameState import BotGameState, BotMove
from src.bots.strategy.Random import Random
from src.bots.strategy.Strategy import Strategy


class FatBot(BaseBot):
    """
    A Bot which attempts to play the most dominoes it can on the first turn.
    """

    first_turn_moves = []

    def __init__(self, strategy: Strategy=Random()):
        """
        Create a FatBot following the specified strategy.
        :param strategy: The Strategy to use.
        """
        super().__init__()
        self.strategy = strategy

    # TODO: Somehow it's playing the same move twice in a row. No idea what's causing it :'(
    def get_move(self, game_state: BotGameState):
        if self.turn == 0:
            if len(self.first_turn_moves) == 0:
                self.first_turn_moves = self.get_move_list_for_biggest_play_from(game_state, self.strategy,
                                                                                 game_state.get_playable_numbers())
            if len(self.first_turn_moves) > 0:
                move = self.first_turn_moves.pop(0)
                return move
        move = self.get_valid_move(game_state, self.strategy)
        return move

    def report_invalid_move(self, move: BotMove):
        super(FatBot, self).report_invalid_move(move)
        self.first_turn_moves = []

    def new_round(self, round_number: int):
        super(FatBot, self).new_round(round_number)
        self.first_turn_moves = []
