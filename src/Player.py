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
        self.can_play = True

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.identity == other.identity

    def __hash__(self):
        return hash(self.identity)

    def __repr__(self):
        return "Player {}".format(self.identity)

    def __str__(self):
        return "Player {} - Victories {}, Score {}".format(self.identity.id, self.victories, self.score)

    def give_domino(self, domino):
        if self.dominoes.count(domino) > 0:
            print("OMG")
        self.dominoes.append(domino)

    def end_round(self, victor):
        if victor:
            self.victories += 1
        self.score += self.calc_score()
        self.dominoes = []
        self.turn = 0
        self.can_play = True

    def calc_score(self):
        score = 0
        for domino in self.dominoes:
            score += domino.left
            score += domino.right
        return score
