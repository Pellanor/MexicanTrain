import abc
from src.bots.state import BotGameState


class TrainChooser:
    """
    A class which will select a Train from a list of trains.
    """

    @abc.abstractmethod
    def choose_trains(self, game_state: BotGameState, trains):
        """
        Choose trains from a list of trains
        :param game_state: The BotGameState for the current turn
        :param trains: the trains to choose from
        :return: a subset of trains
        """
        return

    @staticmethod
    def get_results(chosen_trains, trains):
        """
        Helper method to reduce copy / pasta.
        When choosing a train, if no trains match the chooser, instead just return the original input.
        :param chosen_trains: List of filtered trains
        :param trains: original trains
        :return: list of trains
        """
        if len(chosen_trains) > 0:
            return chosen_trains
        return trains
