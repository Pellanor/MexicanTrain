import abc

from src.bots.state import BotGameState


class PlayChooser:
    """
    A class which will select a Play from a list of plays.
    """

    @abc.abstractmethod
    def choose_plays(self, game_state: BotGameState, plays):
        """
        Choose plays from the input plays list
        :param game_state: The BotGameState for the current turn
        :param plays: The Plays to choose form
        :return: A subset of plays
        """
        return

    @staticmethod
    def get_all_trains_for_plays(plays, trains):
        """
        Helper function to get all valid plays for the specified trains.
        :param plays: The paths to choose from
        :param trains: The trains to get valid plays for
        :return: the subset of plays which match the trains
        """
        return [[train for train in trains if train.requires in play.starts_required] for play in plays]

    @staticmethod
    def get_results(chosen_plays, plays):
        """
        Helper method to reduce copy / pasta.
        When choosing a play, if no plays match the chooser, instead just return the original input.
        :param chosen_plays: List of filtered moves
        :param plays: original plays
        :return: list of plays
        """
        if len(chosen_plays) > 0:
            return chosen_plays
        return plays

