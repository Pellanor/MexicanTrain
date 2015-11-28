import abc
from src.bots.state import BotGameState


class MoveChooser:
    """
    A class which will select a move from a list of moves.
    """

    @abc.abstractmethod
    def choose_moves(self, game_state: BotGameState, moves):
        """
        Choose moves from the input move list.
        :param game_state: The BotGameState for the current turn
        :param moves: a list of Moves to choose from
        :return: A subset of moves matching the desired criteria
        """
        return

    @staticmethod
    def get_results(chosen_moves, moves):
        """
        Helper method to reduce copy / pasta.
        When choosing a move, if no moves match the chooser, instead just return the original input.
        :param chosen_moves: List of filtered moves
        :param moves: original moves
        :return: list of moves
        """
        if len(chosen_moves) > 0:
            return chosen_moves
        return moves
