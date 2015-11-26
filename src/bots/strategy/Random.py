from random import shuffle
from src.bots.state import BotGameState
from src.bots.state.BotGameState import Path
from src.bots.strategy.Strategy import Strategy


class Random(Strategy):
    def choose_train_for_path(self, game_state: BotGameState, path: Path, used_trains=None):
        trains = game_state.trains_for_number[path.start]
        shuffle(trains)
        for train in trains:
            if not used_trains or used_trains.count(train) == 0:
                return train
        return None

    def choose_move(self, moves, game_state: BotGameState):
        if len(moves) > 0:
            shuffle(moves)
            return moves.pop()
        return None

    def choose_path(self, paths, game_state: BotGameState) -> Path:
        if len(paths) > 0:
            shuffle(paths)
            return paths.pop()
        return None

    def choose_play(self, plays, game_state: BotGameState):
        if len(plays) > 0:
            shuffle(plays)
            return plays.pop()
        return None
