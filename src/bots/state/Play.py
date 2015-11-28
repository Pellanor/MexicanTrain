class Play:
    """
    A Play is a Path set sharing no dominoes between them.
    This class adds some convenience functions to the Path set.
    """

    def __init__(self, paths):
        """
        :param paths: the set of paths that make up this play
        """
        self.paths = tuple(paths)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.paths == other.paths

    def __hash__(self):
        return hash(self.paths)

    def __str__(self):
        return str(self.paths)

    @property
    def size(self):
        """
        :return: Number of edges (dominoes) in the play
        """
        return sum([path.size for path in self.paths])

    def get_paths_from(self, origin: int):
        """
        Get all paths in the play starting on the specified origin.
        :param origin: desired start point
        :return: subset of paths which start at the desired point
        """
        return [path for path in self.paths if path.start == origin]

    @property
    def score(self) -> int:
        """
        :return: The number of points contained within the play
        """
        return sum([path.score for path in self.paths])

    @property
    def satisfaction_count(self) -> int:
        """
        Get the number of Paths which demand satisfaction
        :return: the number of Paths which demand satisfaction
        """
        return len([path for path in self.paths if path.demands_satisfaction])

    @property
    def starts_required(self):
        """
        The start points required to satisfy this play
        :return: a tuple of start numbers
        """
        return tuple(path.start for path in self.paths if path.size > 0)

    @property
    def ends(self):
        """
        The end points for this play
        :return: a tuple of end numbers
        """
        return tuple(path.end for path in self.paths if path.size > 0)

    @property
    def demands_satisfaction(self) -> bool:
        """
        :return: A boolean indicating if the last domino in the path is a double
        """
        return self.satisfaction_count > 0
