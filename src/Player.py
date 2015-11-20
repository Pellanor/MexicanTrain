from collections import namedtuple

PlayerIdentity = namedtuple('PlayerIdentity', ['id'])


class Player:
    def __init__(self, player_id, bot):
        self.dominoes = []
        self.identity = PlayerIdentity(player_id)
        self.turn = 0
        self.victories = 0
        self.score = 0
        self.bot = bot

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.identity == other.identity

    def __hash__(self):
        return hash(self.identity)

    def give_domino(self, domino):
        self.dominoes.append(domino)

    def end_round(self, victor):
        if victor:
            self.victories += 1
        self.score += self.calc_score()

    def calc_score(self):
        score = 0
        for domino in self.dominoes:
            score += domino.left
            score += domino.right
        return score
