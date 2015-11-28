class Domino(tuple):
    """
    A Tuple representing a domino. Basically just two numbers, one on the left, the other on the right.
    """

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
        """
        Create a new Domino.
        Automatically ensures that the left is always smaller, so that [2, 3] == [3, 2]
        :param left: the number on the left of the domino.
        :param right:  the number of the right of the domino.
        :return: the new domino!
        """
        return tuple.__new__(cls, (cls._MARKER, min(left, right), max(left, right)))

    def __repr__(self):
        return self.draw(self.left)

    def __str__(self):
        return self.draw(self.left)

    def draw(self, first):
        """
        Draw the domino, with the specified side drawn on the left.
        :param first: the number to draw on the left.
        :return: a String representation of the domino.
        """
        if self.is_double:
            return "[ {} ]".format(self.left)
        return "[{}|{}]".format(first, self.get_other_number(first))

    def contains(self, number) -> bool:
        """
        Returns true if the number is contained in the domino.
        :param number: the number to check
        :return: true if the number is in the domino
        """
        return self.left == number or self.right == number

    @property
    def is_double(self) -> bool:
        """
        :return: True if both sides of the domino are equal
        """
        return self.left == self.right

    def matches(self, domino) -> bool:
        """
        Check if two dominoes can be played next to each other.
        :param domino: The Domino to check against.
        :return: true if they share a number, false otherwise.
        """
        return self.contains(domino.left) or self.contains(domino.right)

    def get_other_number(self, number) -> int:
        """
        Get the other side of the domino.
        :param number: The number of side you don't want.
        :return: for a domino [2|3] calling this with 2 returns 3, and calling with 3 returns 2.
        """
        if self.left == number:
            return self.right
        elif self.right == number:
            return self.left
        else:
            return None


def make_domino_from_edge(edge) -> Domino:
    """
    Helper function for creating a domino from an edge.
    Useful when working with NetworkX graphs.
    :param edge: The edge to convert
    :return: The corresponding Domino
    """
    return Domino(edge[0], edge[1])
