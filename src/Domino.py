class Domino:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "(" + str(self.left) + ", " + str(self.right) + ")"

    def contains(self, number):
        return self.left == number or self.right == number

    def is_double(self):
        return self.left == self.right
