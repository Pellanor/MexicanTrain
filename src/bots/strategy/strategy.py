import abc

from src.Train import Train
from src.bots.state import BotGameState
from src.bots.state.BotGameState import BotMove
from src.bots.state.Play import Play


class Strategy:
    """
    A Strategy can be called to choose from a list of moves, paths, trains, or plays.
    """

    @abc.abstractmethod
    def choose_move(self, game_state: BotGameState, moves) -> BotMove:
        """
        Choose a move from the specified move list.
        :param game_state: the BotGameState for the current turn.
        :param moves: A list of moves to choose from.
        :return: A BotMove from the original list.
        :rtype: BotMove
        """
        return

    @abc.abstractmethod
    def choose_path_and_train(self, game_state: BotGameState, paths, trains):
        """
        Choose a Path and a Train to play the Path on.
        :param game_state: the BotGameState for the current turn.
        :param paths: A list of Paths to choose from.
        :param trains: A list of Trains to choose from.
        :return: A Path and a Train from the original lists.
        :rtype: Path, Train
        """
        return

    @abc.abstractmethod
    def choose_play(self, game_state: BotGameState, plays) -> Play:
        """
        Choose a play from the specified list.
        :param game_state: the BotGameState for the current turn.
        :param plays: a list of Plays to choose form.
        :return: A Play from the original list.
        :rtype: Play
        """
        return

    @abc.abstractmethod
    def choose_train_for_path(self, game_state: BotGameState, path, used_trains) -> Train:
        """
        Choose a play from the specified list.
        :param game_state: the BotGameState for the current turn.
        :param path: The path that will be played on the chosen train.
        :param used_trains: The trains that have already been played on this turn.
        :return: A Train from the original list.
        :rtype: Train
        """
        return
