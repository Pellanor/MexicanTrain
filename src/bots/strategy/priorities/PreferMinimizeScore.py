import abc
from src.bots.state import BotGameState
from src.bots.strategy.MoveChooser import MoveChooser
from src.bots.strategy.PathAndTrainChooser import PathAndTrainChooser
from src.bots.strategy.PlayChooser import PlayChooser


class PreferPlayed(MoveChooser, PlayChooser, PathAndTrainChooser, metaclass=abc.ABCMeta):
    """
    An implementation of MoveChooser, PathAndTrainChooser, and PlayChooser.
    This preference will try to end a train with tiles of the specified number.
    """

    @abc.abstractmethod
    def played_numb_from_moves(self, game_state: BotGameState, moves) -> int:
        """
        Method to determine which number the train should end on
        :param game_state: The BotGameState for the current turn
        :param moves: The moves that are been chosen between
        :return: The desired end number
        """
        return

    @abc.abstractmethod
    def played_numb_from_paths(self, game_state, paths) -> int:
        """
        Method to determine which number the train should end on
        :param game_state: The BotGameState for the current turn
        :param paths: The paths that are been chosen between
        :return: The desired end number
        """
        return

    @abc.abstractmethod
    def played_numb_from_plays(self, game_state, plays) -> int:
        """
        Method to determine which number the train should end on
        :param game_state: The BotGameState for the current turn
        :param plays: The plays that are been chosen between
        :return: The desired end number
        """
        return

    def choose_plays(self, game_state: BotGameState, plays):
        played_numb = self.played_numb_from_plays(game_state, plays)
        chosen_plays = [play for play in plays if
                        sum([game_state.played_count[end] for end in play.ends]) == played_numb]
        if len(chosen_plays) > 0:
            return chosen_plays
        return plays

    def choose_moves(self, game_state: BotGameState, moves):
        played_numb = self.played_numb_from_moves(game_state, moves)
        chosen_moves = [move for move in moves if
                        game_state.played_count[move.domino.get_other_number(move.train.requires)] == played_numb]
        return MoveChooser.get_results(chosen_moves, moves)

    def choose_paths_and_trains(self, game_state: BotGameState, paths, trains):
        played_numb = self.played_numb_from_paths(game_state, paths)
        chosen_paths = [path for path in paths if game_state.played_count[path.end] == played_numb]
        if len(chosen_paths) > 0:
            return chosen_paths, PathAndTrainChooser.get_all_trains_for_paths(chosen_paths, trains)
        return paths, trains
