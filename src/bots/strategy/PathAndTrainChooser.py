import abc
from src.bots.state import BotGameState


class PathAndTrainChooser:
    """
    A class which will select a path and train from a list of paths and trains.
    """

    @abc.abstractmethod
    def choose_paths_and_trains(self, game_state: BotGameState, paths, trains):
        """
        Choose paths and trains from the input path and trains list.
        :param game_state: The BotGameState for the current turn
        :param paths: The paths to choose form.
        :param trains: The trains to choose from
        :return: the chosen paths and trains
        """
        return

    @staticmethod
    def get_all_trains_for_paths(paths, trains):
        """
        Helper function to get all valid trains for the specified paths.
        :param paths: The paths to get valid trains for
        :param trains: The trains to choose from
        :return: the subset of trains which match the paths
        """
        return [train for train in trains if train.requires in (path.start for path in paths)]

    @staticmethod
    def get_all_paths_for_trains(paths, trains):
        """
        Helper function to get all valid paths for the specified trains.
        :param paths: The paths to choose from
        :param trains: The trains to get valid paths for
        :return: the subset of paths which match the trains
        """
        return [path for path in paths if path.start in (train.requires for train in trains)]
