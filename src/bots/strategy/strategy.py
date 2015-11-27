import abc

from src.bots.state import BotGameState
from src.bots.state.BotGameState import BotMove
from src.bots.state.Play import Play


class Strategy:
    @abc.abstractmethod
    def choose_move(self, moves, game_state: BotGameState) -> BotMove:
        return

    @abc.abstractmethod
    def choose_path_and_train(self, game_state: BotGameState, paths, trains):
        return

    @abc.abstractmethod
    def choose_play(self, plays, game_state: BotGameState) -> Play:
        return

    @abc.abstractmethod
    def choose_train_for_path(self, game_state, path, used_trains):
        return

