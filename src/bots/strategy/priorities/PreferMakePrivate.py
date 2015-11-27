from src.bots.state import BotGameState
from src.bots.strategy.MoveChooser import MoveChooser
from src.bots.strategy.PathAndTrainChooser import PathAndTrainChooser
from src.bots.strategy.PlayChooser import PlayChooser
from src.bots.strategy.TrainChooser import TrainChooser


class PreferMakePrivate(TrainChooser, MoveChooser, PathAndTrainChooser, PlayChooser):
    def choose_plays(self, game_state: BotGameState, plays):
        if not game_state.my_train.is_public:
            return plays
        target_start = game_state.my_train.requires
        chosen_plays = [play for play in plays if target_start in play.starts_required]
        return PlayChooser.get_results(chosen_plays, plays)

    def choose_paths_and_trains(self, game_state: BotGameState, paths, trains):
        chosen_trains = self.choose_trains(game_state, trains)
        if len(chosen_trains) > 0:
            return PathAndTrainChooser.get_all_paths_for_trains(paths, chosen_trains), chosen_trains
        return paths, trains

    def choose_trains(self, game_state: BotGameState, trains):
        if game_state.my_train.is_public and game_state.my_train in trains:
            return [game_state.my_train]
        return trains

    def choose_moves(self, game_state: BotGameState, moves):
        if not game_state.my_train.is_public:
            return moves
        chosen_moves = [move for move in moves if move.train == game_state.my_train]
        return MoveChooser.get_results(chosen_moves, moves)
