from src.bots.state import BotGameState
from src.bots.strategy.MoveChooser import MoveChooser
from src.bots.strategy.PathAndTrainChooser import PathAndTrainChooser
from src.bots.strategy.PlayChooser import PlayChooser
from src.bots.strategy.TrainChooser import TrainChooser


def get_fewest(game_state: BotGameState) -> int:
    """
    Get's the lowest number of remaining tiles.
    :param game_state: The BotGameState for the current turn
    :return: the lowest number of remaining tiles
    """
    return min([player.tile_count for player in game_state.players if not player.is_me])


class PreferFewestTiles(TrainChooser, MoveChooser, PathAndTrainChooser, PlayChooser):
    """
    An implementation of TrainChooser, MoveChooser, PathAndTrainChooser, and PlayChooser.
    This preference will try to play on the train of whoever has the fewest dominoes remaining in their hand.
    """
    def choose_plays(self, game_state: BotGameState, plays):
        target_starts = set([train.requires for train in self.choose_trains(game_state, game_state.playable_trains)])
        chosen_plays = [play for play in plays if len(set(play.starts_required).intersection(target_starts)) > 0]
        return PlayChooser.get_results(chosen_plays, plays)

    def choose_paths_and_trains(self, game_state: BotGameState, paths, trains):
        chosen_trains = self.choose_trains(game_state, trains)
        if len(chosen_trains) > 0:
            return PathAndTrainChooser.get_all_paths_for_trains(paths, chosen_trains), chosen_trains
        return paths, trains

    def choose_trains(self, game_state: BotGameState, trains):
        fewest_tiles = get_fewest(game_state)
        chosen_trains = [train for train in trains if train.owner_tile_count == fewest_tiles and not train.am_owner]
        return TrainChooser.get_results(chosen_trains, trains)

    def choose_moves(self, game_state: BotGameState, moves):
        fewest_tiles = get_fewest(game_state)
        chosen_moves = [move for move in moves if
                        move.train.owner_tile_count == fewest_tiles and not move.train.am_owner]
        return MoveChooser.get_results(chosen_moves, moves)
