class Train:
    def __init__(self, train_id, initial, owner):
        self.identity = TrainIdentity(train_id, owner)
        self.private = not self.identity.mexican
        self.requires = initial
        self.demands_satisfaction = False
        self.cars = []

    def add_domino(self, domino, player):
        if self.can_player_add(player):
            if self.__append_left(domino) or self.__append_right(domino):
                if player == self.identity.owner:
                    self.make_private()
                return True
            else:
                return False
        else:
            return False

    def can_player_add(self, player):
        return self.private is False or self.identity.owner == player

    def __append_left(self, domino):
        if self.requires == domino.left:
            self.__append_domino(domino)
            self.requires = domino.right
            return True
        return False

    def __append_right(self, domino):
        if self.requires == domino.right:
            self.__append_domino(domino)
            self.requires = domino.left
            return True
        return False

    def __append_domino(self, domino):
        self.cars.append(domino)
        self.demands_satisfaction = (domino.left == domino.right)

    def make_private(self):
        self.private = True

    def make_public(self):
        self.private = False

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.train_id == other.train_id

    def __hash__(self):
        return hash(self.train_id)


class TrainIdentity(tuple):
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
