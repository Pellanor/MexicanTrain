import abc
from operator import attrgetter

from src.Domino import make_domino_from_edge
from src.bots.state.BotGameState import BotGameState, BotMove
from src.bots.strategy.Strategy import Strategy


class BaseBot:
    """
    Base class for Bpts.
    Has a serious of helper methods that can be used to speed bot development.
    """

    def __init__(self):
        self.invalid_moves = []
        self.turn = 0
        self.round = 0

    def new_round(self, round_number: int):
        """
        Called at the start of every round.
        The rounds start at 12 and count down to 0 (inclusive)
        :param round_number: the current round number
        """
        self.turn = 0
        self.round = round_number

    def start_turn(self, turn_number: int):
        """
        Called at the start of every turn for this bot.
        The first turn is turn 0.
        :param turn_number: the current turn number
        """
        self.turn = turn_number

    @abc.abstractmethod
    def get_move(self, game_state: BotGameState) -> BotMove:
        """
        Called every round when the bot can take a turn
        In the first turn this will be called repeatedly until there are no more possible moves
        On subsequent turns this will only be called once
         If a play is not possible a new tile is drawn and this will be called an additional time
         If a double is played an additional tile can be played and this will be called an additional time
        :param game_state: the BotGameState for the current turn.
        :return: A BotGameState.BotMove which is the move the bot wishes to execute
            Returns None if there are no possible moves.
        :rtype: BotMove
        """
        return

    def report_invalid_move(self, move: BotMove):
        """
        This is called when the game detects that a move is invalid.
        In this case the game will instead choose a random valid move for the game to make.
        :param move: the invalid move that was attempted.
        """
        self.invalid_moves.append((self.round, self.turn, move))

    @staticmethod
    def get_valid_move(game_state: BotGameState, strategy: Strategy) -> BotMove:
        """
        Get a valid move for the bot using the specified game state and strategy.
        :param game_state: the BotGameState for the current turn.
        :param strategy: The Strategy to use to determine the valid move to return.
        :return: A valid move
        :rtype: BotMove
        """
        return strategy.choose_move(game_state, game_state.get_all_valid_moves())

    @staticmethod
    def get_move_list_for_longest_paths_from(game_state: BotGameState, strategy: Strategy, origin):
        """
        Get a list of moves corresponding to the longest path from the specified origin point.
        :param game_state: the BotGameState for the current turn.
        :param strategy: The Strategy to use to determine the valid move to return.
        :param origin: The number to start on, or an iterable containing start numbers.
            All paths will start with one of those number.
        :return: A list of moves corresponding to the longest path
        :rtype: List(BotMove)
        """
        path, train = strategy.choose_path_and_train(game_state, game_state.get_longest_paths_from(origin),
                                                     game_state.playable_trains)
        return [BotMove(make_domino_from_edge(edge), train) for edge in path.edge_list]

    @staticmethod
    def get_move_list_for_biggest_play_from(game_state: BotGameState, strategy: Strategy, origin):
        """
        Get a list of moves corresponding to the largest play from the specified origin point.
        :param game_state: the BotGameState for the current turn.
        :param strategy: The Strategy to use to determine the valid move to return.
        :param origin: The number to start on, or an iterable containing start numbers.
            All paths will start with one of those number.
        :return:A list of moves corresponding to the largest play
        :rtype: List(BotMove)
        """
        try:
            play = strategy.choose_play(game_state, game_state.get_biggest_plays_from(origin))
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
            moves = BaseBot.get_move_list_for_longest_paths_from(game_state, strategy, origin)

        return moves
