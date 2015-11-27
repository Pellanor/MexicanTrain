import abc
from operator import attrgetter

from src.Domino import make_domino_from_edge
from src.bots.state.BotGameState import BotGameState, BotMove
from src.bots.strategy.Strategy import Strategy


class BaseBot:
    def __init__(self):
        self.invalid_moves = []
        self.turn = 0
        self.round = 0

    def new_round(self, round_number: int):
        self.turn = 0
        self.round = round_number

    # Called every round when the bot can take a turn
    # Return a BotGameState.BotMove which is the move the bot wishes to execute
    # If there are no possible moves, return None
    # In the first turn this will be called repeatedly until there are no more possible moves
    # On subsequent turns this will only be called once
    #  If a play is not possible a new tile is drawn and this will be called an additional time
    #  If a double is played an additional tile can be played and this will be called an additional time
    @abc.abstractmethod
    def get_move(self, game_state: BotGameState):
        return

    # Called at the start of every turn for this bot
    # The first turn is turn 0
    def start_turn(self, turn_number: int):
        self.turn = turn_number

    def report_invalid_move(self, move: BotMove):
        self.invalid_moves.append((self.round, self.turn, move))

    @staticmethod
    def get_valid_move(game_state: BotGameState, strategy: Strategy):
        return strategy.choose_move(game_state.get_all_valid_moves(), game_state)

    @staticmethod
    def get_move_list_for_longest_paths_from(origin: int, game_state: BotGameState, strategy: Strategy):
        path, train = strategy.choose_path_and_train(game_state, game_state.get_longest_paths_from(origin),
                                                     game_state.playable_trains)
        return [BotMove(make_domino_from_edge(edge), train) for edge in path.edge_list]

    @staticmethod
    def get_move_list_for_biggest_play_from(origin: int, game_state: BotGameState, strategy: Strategy):
        try:
            play = strategy.choose_play(game_state.get_biggest_plays_from(origin), game_state)
            moves = []
            used_trains = []
            # Loop through the sorted paths, so that any path which demands satisfaction is last
            for path in sorted(play.paths, key=attrgetter('demands_satisfaction')):
                if path.size > 0:
                    train = strategy.choose_train_for_path(game_state, path, used_trains)
                    used_trains.append(train)
                    moves.extend([BotMove(make_domino_from_edge(edge), train) for edge in path.edge_list])

        except AttributeError as e:
            print(e)
            moves = BaseBot.get_move_list_for_longest_paths_from(origin, game_state, strategy)

        return moves
