from src.bots.BaseBot import BaseBot


class TestBot(BaseBot):
    moves = []

    def draw_tile(self, game_state):
        return self.moves

    def take_turn(self, game_state):
        return self.moves
