from src.bots.BaseBot import BaseBot
from src.bots.state.BotGameState import BotGameState


class TestBot(BaseBot):
    moves = []

    def get_move(self, game_state: BotGameState):
        return self.moves.pop(0)
