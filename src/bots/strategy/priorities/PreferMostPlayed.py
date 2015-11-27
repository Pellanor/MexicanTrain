from src.bots.state import BotGameState
from src.bots.strategy.priorities.PreferPlayed import PreferPlayed


class PreferMostPlayed(PreferPlayed):
    def choose_plays(self, game_state: BotGameState, plays):
        return super(PreferMostPlayed, self).choose_plays(game_state, plays)

    def choose_moves(self, game_state: BotGameState, moves):
        return super(PreferMostPlayed, self).choose_moves(game_state, moves)

    def choose_paths_and_trains(self, game_state: BotGameState, paths, trains):
        return super(PreferMostPlayed, self).choose_paths_and_trains(game_state, paths, trains)

    def played_numb_from_paths(self, game_state, paths):
        return max([game_state.played_count[path.end] for path in paths])

    def played_numb_from_moves(self, game_state: BotGameState, moves):
        return max([game_state.played_count[move.domino.get_other_number(move.train.requires)] for move in moves])

    def played_numb_from_plays(self, game_state: BotGameState, plays):
        return max([sum([game_state.played_count[end] for end in play.ends]) for play in plays])
