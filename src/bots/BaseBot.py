import abc

from src.bots.state.BotGameState import BotGameState, BotMove


class BaseBot:

    def __init__(self):
        self.invalid_moves = []
        self.turn = 0
        self.round = 0

    def new_round(self, round_number: int):
        self.turn = 0
        self.round = round_number

    # Called every round when the bot can take a turn
    # Return a BotGameState.BotMove which is the move the bot wishes to execute
    # If there are no possible moves, return None
    # In the first turn this will be called repeatedly until there are no more possible moves
    # On subsequent turns this will only be called once
    #  If a play is not possible a new tile is drawn and this will be called an additional time
    #  If a double is played an additional tile can be played and this will be called an additional time
    @abc.abstractmethod
    def get_move(self, game_state: BotGameState):
        return

    # Called at the start of every turn for this bot
    # The first turn is turn 0
    def start_turn(self, turn_number: int):
        self.turn = turn_number

    def report_invalid_move(self, move: BotMove):
        self.invalid_moves.append((self.round, self.turn, move))
