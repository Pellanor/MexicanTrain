from random import shuffle
from src.bots.BaseBot import BaseBot
from src.bots.state.BotGameState import BotGameState


class RandomBot(BaseBot):

    def get_move(self, game_state: BotGameState):
        possible_moves = game_state.get_all_valid_moves()
        if len(possible_moves) > 0:
            shuffle(possible_moves)
            return possible_moves.pop()
        return None

