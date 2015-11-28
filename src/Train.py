from src.Domino import Domino
from src.Player import Player


class Train:
    """
    A Train is where dominoes can be played.
    Each train has an owner, and each player can play on a given train according to certain rules.
    """

    def __init__(self, train_id: int, initial: int, owner):
        """
        Create a new train.
        :param train_id: The ID for the train. Should be unique.
        :param initial: The starting number that cna be played on the train.
        :param owner: The Player who owns the current train. Specify None for the mexican train.
        """
        self.identity = TrainIdentity(train_id, owner)
        self.private = not self.identity.mexican
        self.initial = self.requires = initial
        self.demands_satisfaction = False
        self.cars = []

    def is_valid_play(self, domino: Domino, player: Player) -> bool:
        """
        Assert if the player is allowed to place the specified domino on this train.
        :param domino: the Domino to be placed.
        :param player: the Player attempting to place it.
        :return: True if play is allowed, False otherwise.
        """
        return self.can_player_add(player) and domino.contains(self.requires)

    def add_domino(self, domino: Domino, player: Player) -> bool:
        """
        Attempt to add the domino to the end of the Train.
        :param domino: the Domino to add.
        :param player: the Player adding it.
        :return: True if play is allowed, False otherwise.
        """
        if self.can_player_add(player):
            if self.__append_left(domino) or self.__append_right(domino):
                if self.private and self.demands_satisfaction:
                    # Whenever you play a double on your train, it becomes public until you play on your train again.
                    self.make_public()
                elif player == self.identity.owner:
                    # When you play on your own train and it's not a double, it is made private.
                    self.make_private()
                return True
            else:
                return False
        else:
            return False

    def can_player_add(self, player: Player):
        """
        Assert if the player is allowed to play on the train.
        :param player: the Player attempting to play.
        :return: True if play is allowed, False otherwise.
        """
        return self.private is False or self.identity.owner == player

    def __append_left(self, domino: Domino):
        if self.requires == domino.left:
            self.__append_domino(domino)
            self.requires = domino.right
            return True
        return False

    def __append_right(self, domino: Domino):
        if self.requires == domino.right:
            self.__append_domino(domino)
            self.requires = domino.left
            return True
        return False

    def __append_domino(self, domino: Domino):
        self.cars.append(domino)
        self.demands_satisfaction = (domino.left == domino.right)

    def make_private(self):
        """ Make the train private """
        self.private = True

    def make_public(self):
        """ Make the train public """
        self.private = False

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.identity == other.identity

    def __hash__(self):
        return hash(self.identity)

    def __repr__(self):
        return "Train {}".format(self.identity)

    def __str__(self):
        if self.identity.mexican:
            output = "Mexican Train: "
        else:
            output = "Player {}'s Train: ".format(self.identity.owner.identity.id)
        left = self.initial
        for domino in self.cars:
            output += "{} ".format(domino.draw(left))
            left = domino.get_other_number(left)
        return output


class TrainIdentity(tuple):
    """
    An Immutable, hashable identifier for each train.
    """

    @property
    def train_id(self):
        return self[1]

    @property
    def owner(self):
        return self[2]

    @property
    def mexican(self):
        return self[3]

    __slots__ = ()
    # An immutable and unique marker, used to make sure different
    # tuple subclasses are not equal to each other.
    _MARKER = object()

    def __new__(cls, train_id, owner):
        return tuple.__new__(cls, (cls._MARKER, train_id, owner, owner is None))

    def __init__(self, train_id, owner):
        super().__init__()
