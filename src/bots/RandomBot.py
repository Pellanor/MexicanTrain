from random import shuffle

from src.bots.BaseBot import BaseBot


class RandomBot(BaseBot):
    def take_first_turn(self):
        while self.take_turn():
            continue

    def take_turn(self):
        dominoes = self.game_state.get_dominoes()
        shuffle(dominoes)
        ends = self.game_state.get_playable_train_ends()
        for domino in dominoes:
            for end in ends:
                train, requires = end.get_train_end()
                if domino.contains(requires):
                    if self.game_state.place_domino(self.game_state.get_domino_id(domino), train):
                        return True
