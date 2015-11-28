from collections import namedtuple

from src.Domino import Domino

PlayerIdentity = namedtuple('PlayerIdentity', ['id'])


class Player:
    """
    A representation of somebody playing the game.
    """

    def __init__(self, player_id, bot):
        """
        Create a new player with an appropriate ID and Bot
        :param player_id:
        :param bot:
        """
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

    def give_domino(self, domino: Domino):
        """
        Give the specified domino ot the player, putting it in their "hand"
        :param domino: The Domino to give.
        """
        if self.dominoes.count(domino) > 0:
            print("OMG")
        self.dominoes.append(domino)

    def end_round(self, victor):
        """
        Specify the end of the current round.
        :param victor: If the player won the round.
        """
        if victor:
            self.victories += 1
        self.score += self.calc_score()
        self.dominoes = []
        self.turn = 0
        self.can_play = True

    def calc_score(self):
        """
        Get the score for the current "hand" of dominoes. Lower is better.
        """
        return sum([domino.left + domino.right for domino in self.dominoes])
