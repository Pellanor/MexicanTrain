from random import shuffle

from src.bots.state import BotGameState
from src.bots.strategy.MoveChooser import MoveChooser
from src.bots.strategy.PathAndTrainChooser import PathAndTrainChooser
from src.bots.strategy.PlayChooser import PlayChooser
from src.bots.strategy.TrainChooser import TrainChooser


class PreferRandom(TrainChooser, MoveChooser, PathAndTrainChooser, PlayChooser):
    """
    An implementation of TrainChooser, MoveChooser, PathAndTrainChooser, and PlayChooser.
    This preference will just pick at random.
    Every Preference chain should end with PreferRandom to ensure that only a single result is selected.
    """

    def choose_plays(self, game_state: BotGameState, plays):
        shuffle(plays)
        return [plays.pop()]

    def choose_paths_and_trains(self, game_state: BotGameState, paths, trains):
        shuffle(paths)
        path = paths.pop()
        chosen_trains = [train for train in trains if train.requires == path.start]
        train = self.choose_trains(game_state, chosen_trains)
        return [path], train  # train is not a list since choose_trains returns a list

    def choose_trains(self, game_state: BotGameState, trains):
        shuffle(trains)
        return [trains.pop()]

    def choose_moves(self, game_state: BotGameState, moves):
        shuffle(moves)
        return [moves.pop()]
