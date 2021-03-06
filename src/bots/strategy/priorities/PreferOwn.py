from src.bots.state import BotGameState
from src.bots.strategy.MoveChooser import MoveChooser
from src.bots.strategy.PathAndTrainChooser import PathAndTrainChooser
from src.bots.strategy.PlayChooser import PlayChooser
from src.bots.strategy.TrainChooser import TrainChooser


class PreferOwn(TrainChooser, MoveChooser, PathAndTrainChooser, PlayChooser):
    """
    An implementation of TrainChooser, MoveChooser, PathAndTrainChooser, and PlayChooser.
    This preference will try to play on your own train.
    """

    def choose_plays(self, game_state: BotGameState, plays):
        target_start = game_state.my_train.requires
        chosen_plays = [play for play in plays if target_start in play.starts_required]
        return PlayChooser.get_results(chosen_plays, plays)

    def choose_paths_and_trains(self, game_state: BotGameState, paths, trains):
        chosen_trains = self.choose_trains(game_state, trains)
        if len(chosen_trains) > 0:
            chosen_paths = PathAndTrainChooser.get_all_paths_for_trains(paths, chosen_trains)
            if len(chosen_paths) > 0:
                return chosen_paths, chosen_trains
        return paths, trains

    def choose_trains(self, game_state: BotGameState, trains):
        chosen_trains = [train for train in trains if train.am_owner]
        return TrainChooser.get_results(chosen_trains, trains)

    def choose_moves(self, game_state: BotGameState, moves):
        chosen_moves = [move for move in moves if move.train.am_owner]
        return MoveChooser.get_results(chosen_moves, moves)
