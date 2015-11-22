from src.Domino import Domino


class BotDomino:

    def __init__(self, domino: Domino):
        self.value = domino
        self.left = []
        self.right = []

    def add_domino(self, bot_domino):
        if bot_domino.value.contains(self.value.left):
            self.left.append(bot_domino)
        if bot_domino.value.contains(self.value.right):
            self.right.append(bot_domino)

    def add_all(self, dominoes):
        for bot_domino in dominoes:
            self.add_domino(bot_domino)

    def remove_domino(self, bot_domino):
        if self.left.count(bot_domino) > 0:
            self.left.remove(bot_domino)
        if self.right.count(bot_domino) > 0:
            self.right.remove(bot_domino)

    def play(self):
        for bot_domino in self.left + self.right:
            bot_domino.remove_domino(self)