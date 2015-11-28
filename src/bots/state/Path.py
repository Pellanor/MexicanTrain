class Path:
    """
    A Path is a list of edges by which the domino graph can be traversed.
    It is equivalent to list of dominoes played in order.
    """

    def __init__(self, edge_list):
        self.edge_list = edge_list
        self.edge_set = None
        self.edge_tuple = None

    def get_edge_set(self):
        if self.edge_set is None:
            self.edge_set = set([Path.key(edge) for edge in self.edge_list])
        return self.edge_set

    def get_edge_tuple(self):
        if self.edge_tuple is None:
            self.edge_tuple = tuple([Path.key(edge) for edge in self.edge_list])

    @property
    def size(self) -> int:
        """
        :return: Number of edges (dominoes) in the path
        """
        return len(self.edge_list)

    @property
    def start(self) -> int:
        """
        :return: The number which the path starts on
        """
        if self.size > 0:
            return self.edge_list[0][0]
        return None

    @property
    def end(self) -> int:
        """
        :return: The number which the path ends on
        """
        if self.size > 0:
            return self.edge_list[-1][1]
        return None

    @property
    def score(self) -> int:
        """
        :return: The number of points contained within the path
        """
        return sum([edge[0] + edge[1] for edge in self.edge_list])

    @property
    def demands_satisfaction(self) -> bool:
        """
        :return: A boolean indicating if the last domino in the path is a double
        """
        if self.size > 0:
            return self.edge_list[-1][0] == self.edge_list[-1][1]
        return False

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.get_edge_tuple() == other.get_edge_tuple()

    def __hash__(self):
        return hash(self.get_edge_tuple())

    def __str__(self):
        return str(self.edge_list)

    @staticmethod
    def key(edge):
        """
        Function for creating a hashable version of an edge.
        From NetworkX edgedfs.py
        :param edge: the edge to hash
        :return: a hashable version of the provided edge
        """
        new_edge = (frozenset(edge[:2]),) + edge[2:]
        return new_edge
