class Path:
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
    def size(self):
        return len(self.edge_list)

    @property
    def start(self):
        if self.size > 0:
            return self.edge_list[0][0]
        return None

    @property
    def end(self):
        if self.size > 0:
            return self.edge_list[-1][1]
        return None

    @property
    def demands_satisfaction(self):
        if self.size > 0:
            return self.edge_list[-1][0] == self.edge_list[-1][1]
        return False

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.get_edge_tuple() == other.get_edge_tuple()

    def __hash__(self):
        return hash(self.get_edge_tuple())

    def __str__(self):
        return str(self.edge_list)

    # From NetworkX edgedfs.py
    @staticmethod
    def key(edge):
        new_edge = (frozenset(edge[:2]),) + edge[2:]
        return new_edge
