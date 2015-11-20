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
        return tuple.__new__(cls, (cls._MARKER, left, right))

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.left, self.right)

    def __str__(self):
        return "(" + str(self.left) + ", " + str(self.right) + ")"

    def contains(self, number):
        return self.left == number or self.right == number

    @property
    def is_double(self):
        return self.left == self.right

    def get_other_number(self, number):
        if self.left == number:
            return self.right
        elif self.right == number:
            return self.left
        else:
            return None
