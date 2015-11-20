from random import shuffle
from src.bots.BaseBot import BaseBot
from src.bots.state.BotGameState import BotGameState


class RandomBot(BaseBot):
    def draw_tile(self, game_state: BotGameState):
        return self.get_moves(game_state)

    def take_turn(self, game_state: BotGameState):
        # Must be incremented before getting a move so that the same value is used if we have to call get_moves
        # later because we're forced to draw a tile. This allows us to continue playing multiple tiles.
        self.turn += 1
        return self.get_moves(game_state)

    # Pick one of the possible turns at random
    @staticmethod
    def get_move(game_state: BotGameState):
        possible_moves = game_state.get_all_valid_moves()
        if len(possible_moves) > 0:
            shuffle(possible_moves)
            return possible_moves.pop()
        return False

    # Get a list of moves to take for the turn
    def get_moves(self, game_state: BotGameState):
        moves_to_take = []
        move = self.get_move(game_state)
        if self.turn == 1:
            while move:
                moves_to_take.append(move)
                move = self.get_move(game_state)
        else:
            if move:
                moves_to_take.append(move)
        return moves_to_take
