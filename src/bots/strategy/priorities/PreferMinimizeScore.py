from src.bots.state import BotGameState
from src.bots.strategy.MoveChooser import MoveChooser
from src.bots.strategy.PathAndTrainChooser import PathAndTrainChooser
from src.bots.strategy.PlayChooser import PlayChooser


class PreferMinimizeScore(MoveChooser, PlayChooser, PathAndTrainChooser):
    """
    An implementation of MoveChooser, PathAndTrainChooser, and PlayChooser.
    This preference will try to play the highest "value" dominoes, to keep from being stuck with them at the end.
    """

    def choose_plays(self, game_state: BotGameState, plays):
        target_score = max([play.score for play in plays])
        chosen_plays = [play for play in plays if play.score == target_score]
        if len(chosen_plays) > 0:
            return chosen_plays
        return plays

    def choose_moves(self, game_state: BotGameState, moves):
        target_score = max([move.domino.left + move.domino.right for move in moves])
        chosen_moves = [move for move in moves if move.domino.left + move.domino.right == target_score]
        return MoveChooser.get_results(chosen_moves, moves)

    def choose_paths_and_trains(self, game_state: BotGameState, paths, trains):
        target_score = max([path.score for path in paths])
        chosen_paths = [path for path in paths if path.score == target_score]
        if len(chosen_paths) > 0:
            return chosen_paths, PathAndTrainChooser.get_all_trains_for_paths(chosen_paths, trains)
        return paths, trains
