class Train:
    def __init__(self, train_id, initial, player):
        self.train_id = train_id
        self.owner = player
        self.private = player is not None
        self.requires = initial
        self.demands_satisfaction = False
        self.cars = []

    def add_domino(self, domino, player):
        if self.can_player_add(player):
            if self.__append_left(domino) or self.__append_right(domino):
                if player == self.owner:
                    self.make_private()
                return True
            else:
                return False
        else:
            return False

    def can_player_add(self, player):
        return self.private is False or self.owner is None or self.owner == player

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
