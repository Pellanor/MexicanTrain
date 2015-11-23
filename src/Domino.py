class Domino(tuple):
    @property
    def left(self):
        return self[1]

    @property
    def right(self):
        return self[2]

    __slots__ = ()
    # An immutable and unique marker, used to make sure different
    # tuple subclasses are not equal to each other.
    _MARKER = object()

    def __init__(self, left: int, right: int):
        super().__init__()

    def __new__(cls, left: int, right: int):
        # ensure that the left is always smaller, so that [2, 3] == [3, 2]
        return tuple.__new__(cls, (cls._MARKER, min(left, right), max(left, right)))

    def __repr__(self):
        return self.draw(self.left)

    def __str__(self):
        return self.draw(self.left)

    def draw(self, first):
        if self.is_double:
            return "[ {} ]".format(self.left)
        return "[{}|{}]".format(first, self.get_other_number(first))

    def contains(self, number):
        return self.left == number or self.right == number

    @property
    def is_double(self):
        return self.left == self.right

    def matches(self, domino):
        return self.contains(domino.left) or self.contains(domino.right)

    def get_other_number(self, number):
        if self.left == number:
            return self.right
        elif self.right == number:
            return self.left
        else:
            return None


def make_domino_from_edge(edge):
    return Domino(edge[0], edge[1])
