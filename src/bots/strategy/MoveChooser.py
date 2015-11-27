import abc
from src.bots.state import BotGameState


class MoveChooser:
    @abc.abstractmethod
    def choose_moves(self, game_state: BotGameState, moves):
        return

    @staticmethod
    def get_results(chosen_moves, moves):
        if len(chosen_moves) > 0:
            return chosen_moves
        return moves
