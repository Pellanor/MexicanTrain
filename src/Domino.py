class Domino:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.left == other.left and self.right == other.right

    def __hash__(self):
        return self.left * 100 + self.right

    def __str__(self):
        return "(" + str(self.left) + ", " + str(self.right) + ")"

    def contains(self, number):
        return self.left == number or self.right == number

    def is_double(self):
        return self.left == self.right

    def other_number(self, number):
        if self.left == number:
            return self.right
        elif self.right == number:
            return self.left
        else:
            return None
