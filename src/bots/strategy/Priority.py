from src.bots.state import BotGameState
from src.bots.strategy.Strategy import Strategy


class Priority(Strategy):
    def choose_train_for_path(self, game_state, path, used_trains):
        pass

    def choose_move(self, moves, game_state: BotGameState):
        pass

    def choose_path(self, paths, game_state: BotGameState):
        pass

    def choose_play(self, plays, game_state: BotGameState):
        pass