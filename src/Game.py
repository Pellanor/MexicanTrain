from src.GameState import GameState


class Game:
    def __init__(self, player_count):
        self.game_state = GameState(player_count)

    def play(self):
        # self.setup_game()
        for cur_round in range(12, 0, -1):
            self.game_state.start_round(cur_round)
            self.play_round()

    def play_round(self):
        while not self.game_state.round_over:
            self.take_turn()
            self.check_for_victory()
            self.next_player()

    def take_turn(self):
        player = self.current_bot
        if player.turn == 0:
            pass

    def check_for_victory(self):
        pass

    def next_player(self):
        self.current_bot = self.players[self.current_bot.playerId + 1 % len(self.players)]
