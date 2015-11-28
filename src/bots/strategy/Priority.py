from copy import copy
from src.bots.state import BotGameState
from src.bots.state.Path import Path
from src.bots.strategy.MoveChooser import MoveChooser
from src.bots.strategy.PathAndTrainChooser import PathAndTrainChooser
from src.bots.strategy.PlayChooser import PlayChooser
from src.bots.strategy.Strategy import Strategy
from src.bots.strategy.TrainChooser import TrainChooser


class Priority(Strategy):
    """
    A Strategy which will select moves by running them through a priority chain.
    This chain will filter out results based on the various preferences.
    """

    def __init__(self, priority_chain):
        self.priority_chain = priority_chain

    def choose_train_for_path(self, game_state: BotGameState, path: Path, used_trains):
        possible_trains = [train for train in game_state.playable_trains if
                           used_trains.count(train) == 0 and path.start == train.requires]
        for priority in self.priority_chain:
            if isinstance(priority, TrainChooser().__class__):
                possible_trains = priority.choose_trains(game_state, possible_trains)
                if len(possible_trains) == 1:
                    return possible_trains[0]
        raise RuntimeError("Priority Strategy didn't choose a train!\n {}".format(self.priority_chain))

    def choose_move(self, game_state: BotGameState, moves):
        possible_moves = copy(moves)
        for priority in self.priority_chain:
            if isinstance(priority, MoveChooser().__class__):
                possible_moves = priority.choose_moves(game_state, possible_moves)
                if len(possible_moves) == 1:
                    return possible_moves[0]
        raise RuntimeError("Priority Strategy didn't choose a move!\n {}".format(self.priority_chain))

    def choose_path_and_train(self, game_state: BotGameState, paths, trains):
        possible_trains = copy(trains)
        possible_paths = copy(paths)
        for priority in self.priority_chain:
            if isinstance(priority, PathAndTrainChooser().__class__):
                possible_paths, possible_trains = priority.choose_paths_and_trains(game_state, possible_paths,
                                                                                   possible_trains)
                if len(possible_paths) == 1 and len(possible_trains) == 1:
                    return possible_paths[0], possible_trains[0]
        raise RuntimeError("Priority Strategy didn't choose a path!\n {}".format(self.priority_chain))

    def choose_play(self, game_state: BotGameState, plays):
        possible_plays = copy(plays)
        for priority in self.priority_chain:
            if isinstance(priority, PlayChooser().__class__):
                possible_plays = priority.choose_plays(game_state, possible_plays)
                if len(possible_plays) == 1:
                    return possible_plays[0]
        raise RuntimeError("Priority Strategy didn't choose a play!\n {}".format(self.priority_chain))
