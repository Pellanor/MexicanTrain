import abc


class BaseBot:

    def __init__(self):
        self.turn = 0

    def new_round(self, round_number):
        self.turn = 0

    # Called every round when the bot can take a turn
    # Return a list of type BotGameState.Move
    # In the first turn all Moves will be executed in order until the list is exhausted, or an invalid Move is attempted
    # In all subsequent turns only the first Move in the list will be executed
    @abc.abstractmethod
    def take_turn(self, bot_game_state):
        return

    # Called when the bot draws a new tile after being unable to play
    # The BotGameState will be updated to include the new tile
    # Return a list of type BotGameState.Move
    # In the first turn all Moves will be executed in order until the list is exhausted, or an invalid Move is attempted
    # In all subsequent turns only the first Move in the list will be executed
    @abc.abstractmethod
    def draw_tile(self, bot_game_state):
        return

