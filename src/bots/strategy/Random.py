from random import shuffle
from src.bots.state import BotGameState
from src.bots.state.Path import Path
from src.bots.strategy.Strategy import Strategy


class Random(Strategy):
    """
    A Strategy that just picks moves at random.
    """

    def choose_train_for_path(self, game_state: BotGameState, path: Path, used_trains=None):
        trains = game_state.trains_for_number[path.start]
        shuffle(trains)
        for train in trains:
            if not used_trains or used_trains.count(train) == 0:
                return train
        return None

    def choose_move(self, game_state: BotGameState, moves):
        if len(moves) > 0:
            shuffle(moves)
            return moves.pop()
        return None

    def choose_path_and_train(self, game_state: BotGameState, paths, trains) -> Path:
        if len(paths) > 0:
            shuffle(paths)
            path = paths.pop()
            train = self.choose_train_for_path(game_state, path)
            return path, train
        return None

    def choose_play(self, game_state: BotGameState, plays):
        if len(plays) > 0:
            shuffle(plays)
            return plays.pop()
        return None
