from src.bots.state import BotGameState
from src.bots.strategy.priorities.PreferPlayed import PreferPlayed


class PreferLeastPlayed(PreferPlayed):
    """
    An implementation of PreferPlayed
    This will prefer ending with a tile that has been played the fewest times, so has the greatest odds of being drawn.
    """

    def choose_plays(self, game_state: BotGameState, plays):
        return super(PreferLeastPlayed, self).choose_plays(game_state, plays)

    def choose_moves(self, game_state: BotGameState, moves):
        return super(PreferLeastPlayed, self).choose_moves(game_state, moves)

    def choose_paths_and_trains(self, game_state: BotGameState, paths, trains):
        return super(PreferLeastPlayed, self).choose_paths_and_trains(game_state, paths, trains)

    def played_numb_from_paths(self, game_state, paths) -> int:
        return min([game_state.played_count[path.end] for path in paths])

    def played_numb_from_moves(self, game_state: BotGameState, moves) -> int:
        return min([game_state.played_count[move.domino.get_other_number(move.train.requires)] for move in moves])

    def played_numb_from_plays(self, game_state: BotGameState, plays) -> int:
        return min([sum([game_state.played_count[end] for end in play.ends]) for play in plays])


