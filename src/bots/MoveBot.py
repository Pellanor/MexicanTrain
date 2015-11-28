from src.bots.BaseBot import BaseBot
from src.bots.state.BotGameState import BotGameState
from src.bots.strategy.Random import Random


class MoveBot(BaseBot):

    def __init__(self, strategy=Random()):
        super().__init__()
        self.strategy = strategy

    def get_move(self, game_state: BotGameState):
        return self.strategy.choose_move(game_state, game_state.get_all_valid_moves())

