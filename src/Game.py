from random import shuffle
from src.GameState import GameState
from src.Player import Player
from src.Train import Train
from src.bots.state.BotGameState import BotGameState, BotMove


class Game:
    """
    The Game of Mexican Train! Yay! \m/
    """

    def __init__(self, player_count):
        """
        Create a Game for the specified number of players.
        :param player_count: How many players are playing.
        """
        self.game_state = GameState(player_count)

    def play(self, print_each_round=False):
        """
        Play the game!
        :param print_each_round: Flag to print out the results of each round.
        """
        for cur_round in range(12, -1, -1):
            self.game_state.start_round(cur_round)
            self.play_round()
            if print_each_round:
                self.print_round(cur_round)
            self.game_state.clean_up_after_round()

    def play_round(self):
        """
        Play the current round.
        """
        while not self.game_state.round_over:
            self.take_turn()
            self.check_for_victory()
            self.game_state.next_player()

    def take_turn(self):
        """
        Take a turn for the current active player, as determined by the GameState.
        """
        player = self.game_state.current_player
        player.can_play = True
        bot_game_state = BotGameState(self.game_state, player)

        drew = False
        played = False
        done = False
        first = player.turn == 0

        player.bot.start_turn(player.turn)
        while not done:
            valid_moves = bot_game_state.get_all_valid_moves()
            if len(valid_moves) == 0:
                if not played and not drew:
                    domino = self.game_state.draw_domino(player)
                    if not domino:
                        player.can_play = False
                        done = True
                    else:
                        bot_game_state.draw_domino(domino)
                    drew = True
                else:
                    done = True
            else:
                move = player.bot.get_move(bot_game_state)
                if not self.validate_move(move, player):
                    player.bot.report_invalid_move(move)
                    shuffle(valid_moves)
                    move = valid_moves.pop()
                if move.domino.is_double:
                    drew = False
                    played = False
                else:
                    played = True
                self.do_move(player, move)
                bot_game_state.do_move(move)
                if played and not first:
                    done = True
        player.turn += 1

    def validate_move(self, move: BotMove, player: Player) -> bool:
        """
        Validate if a move can be played.
        :param move: The move to attempt
        :param player: The player attempting the move
        :return: True if the move is legal, False otherwise.
        """
        return self.get_train_from_move(move).is_valid_play(move.domino, player) and \
            player.dominoes.count(move.domino) > 0 and \
            self.game_state.played.count(move.domino) == 0

    def get_train_from_move(self, move: BotMove) -> Train:
        """
        Helper method to extract the train from the game state for a given BotMove.
        This is required as the BotMove only contains a reference to the BotTrain.
        :param move: The BotMove to get the train for.
        :return: The corresponding Train.
        """
        return self.game_state.trains[move.train.identity.train_id]

    def do_move(self, player: Player, move: BotMove):
        """
        Actually execute a move!
        :param player: The player making the move.
        :param move: The move the player is attempting to make.
        :return: True if the move was executed successfully.
        """
        if player.dominoes.count(move.domino) == 0:
            raise RuntimeError(
                "Cannot add Domino that player doesn't have! \n Move: {} \n Dominoes {} \n {} \n Played {}".
                format(move, player.dominoes, self.get_train_from_move(move), self.game_state.played))
        if self.game_state.played.count(move.domino) > 0:
            raise RuntimeError(
                "Cannot play a domino that has already been played! \n Move: {} \n Dominoes {} \n {} \n Played {}".
                format(move, player.dominoes, self.get_train_from_move(move), self.game_state.played))
        train = self.get_train_from_move(move)
        if train.add_domino(move.domino, player):
            player.dominoes.remove(move.domino)
            self.game_state.played.append(move.domino)
            return True
        return False

    def check_for_victory(self):
        """
        Check to see if somebody has won. If so tell every player that the round is over.
        """
        player = self.game_state.current_player
        if len(player.dominoes) == 0:
            self.game_state.round_over = True
            self.game_state.round_winner = player
            for p in self.game_state.players:
                p.end_round(p == player)
        else:
            all_cannot_play = True
            for player in self.game_state.players:
                if player.can_play:
                    all_cannot_play = False
                    break
            if all_cannot_play:
                inter_players = iter(self.game_state.players)
                min_player = next(inter_players)
                min_player.score += min_player.calc_score()
                for p in inter_players:
                    if len(p.dominoes) < len(min_player.dominoes) or \
                            (len(p.dominoes) == len(min_player.dominoes) and p.calc_score() < min_player.calc_score()):
                        min_player = p
                self.game_state.round_over = True
                self.game_state.round_winner = min_player
                for p in self.game_state.players:
                    p.end_round(p == min_player)

    def print_round(self, round_numb: int):
        """
        Format the output for the round and print it to the console.
        :param round_numb: The current round number.
        """
        output = "Mexican Train! - Round {} Winner: Player {}!\n". \
            format(round_numb, str(self.game_state.round_winner.identity.id))
        output += '\n'.join([str(player) for player in self.game_state.players])
        output += '\n'
        output += '\n'.join([str(train) for train in self.game_state.trains])
        output += '\n===========================================\n\n'
        print(output)

    def get_stats(self):
        """
        Create a map of player ID to victories + score, for tracking across multiple games.
        :return:
        """
        return {player.identity.id: [player.victories, player.score] for player in self.game_state.players}
