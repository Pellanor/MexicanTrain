from src.bots.BaseBot import BaseBot


class TestBot(BaseBot):
    moves = []

    def draw_tile(self, bot_game_state):
        return self.moves

    def take_turn(self, bot_game_state):
        return self.moves
