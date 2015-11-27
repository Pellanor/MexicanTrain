class Play:
    def __init__(self, paths):
        self.paths = tuple(paths)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.paths == other.paths

    def __hash__(self):
        return hash(self.paths)

    def __str__(self):
        return str(self.paths)

    @property
    def size(self):
        return sum([path.size for path in self.paths])

    def get_paths_from(self, origin: int):
        return [path for path in self.paths if path.start == origin]

    @property
    def satisfaction_count(self):
        return len([path for path in self.paths if path.demands_satisfaction])

    @property
    def starts_required(self):
        return tuple(path.start for path in self.paths if path.size > 0)

    @property
    def ends(self):
        return tuple(path.end for path in self.paths if path.size > 0)

    @property
    def demands_satisfaction(self):
        return self.satisfaction_count > 0
