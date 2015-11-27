import abc
from src.bots.state import BotGameState


class PathAndTrainChooser:
    @abc.abstractmethod
    def choose_paths_and_trains(self, game_state: BotGameState, paths, trains):
        return

    @staticmethod
    def get_all_trains_for_paths(paths, trains):
        return [train for train in trains if train.requires in (path.start for path in paths)]

    @staticmethod
    def get_all_paths_for_trains(paths, trains):
        return [path for path in paths if path.start in (train.requires for train in trains)]
