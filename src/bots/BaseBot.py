import abc


class BaseBot:

    def __init__(self, game_state):
        self.game_state = game_state

    @abc.abstractmethod
    def take_turn(self, game):
        return

    @abc.abstractmethod
    def take_first_turn(self, game):
        return
