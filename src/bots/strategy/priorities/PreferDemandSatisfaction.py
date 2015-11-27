from src.bots.state import BotGameState
from src.bots.strategy.MoveChooser import MoveChooser
from src.bots.strategy.PathAndTrainChooser import PathAndTrainChooser
from src.bots.strategy.PlayChooser import PlayChooser


class PreferDemandSatisfaction(MoveChooser, PathAndTrainChooser, PlayChooser):
    def choose_plays(self, game_state: BotGameState, plays):
        chosen_plays = [play for play in plays if play.demands_satisfaction]
        if len(chosen_plays) > 0:
            return chosen_plays
        return plays

    def choose_paths_and_trains(self, game_state: BotGameState, paths, trains):
        chosen_paths = [path for path in paths if path.demands_satisfaction]
        if len(chosen_paths) > 0:
            return chosen_paths, PathAndTrainChooser.get_all_trains_for_paths(chosen_paths, trains)
        return paths, trains

    def choose_moves(self, game_state: BotGameState, moves):
        chosen_moves = [move for move in moves if move.domino.is_double]
        return MoveChooser.get_results(chosen_moves, moves)
