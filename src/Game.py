from random import shuffle

from src.GameState import GameState, draw_domino
from src.Player import Player
from src.Train import Train
from src.bots.state.BotGameState import BotGameState, BotMove


class Game:
    def __init__(self, player_count):
        self.game_state = GameState(player_count)

    def play(self):
        for cur_round in range(12, -1, -1):
            self.game_state.start_round(cur_round)
            self.play_round()
            self.print_round(cur_round)
            self.game_state.clean_up_after_round()

    def play_round(self):
        while not self.game_state.round_over:
            self.take_turn()
            self.check_for_victory()
            self.game_state.next_player()

    def take_turn(self):
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
                    domino = draw_domino(self.game_state, player)
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
                    shuffle(valid_moves)
                    move = valid_moves.pop()
                if move.domino.value.is_double:
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
        return self.get_train_from_move(move).is_valid_play(move.domino.value, player)

    def get_train_from_move(self, move: BotMove) -> Train:
        return self.game_state.trains[move.train.identity.train_id]

    def do_move(self, player: Player, move: BotMove):
        if player.dominoes.count(move.domino.value) == 0:
            raise RuntimeError("Cannot add Domino that player doesn't have!")
        if self.game_state.played.count(move.domino.value)> 0:
            raise RuntimeError("Cannot play a domino that has already been played!")
        train = self.get_train_from_move(move)
        if train.add_domino(move.domino.value, player):
            player.dominoes.remove(move.domino.value)
            return True
        return False

    def check_for_victory(self):
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
        output = "Mexican Train! - Round {} Winner: Player {}!\n". \
            format(round_numb, str(self.game_state.round_winner.identity.id))
        output += '\n'.join([str(player) for player in self.game_state.players])
        output += '\n'
        output += '\n'.join([str(train) for train in self.game_state.trains])
        output += '\n===========================================\n\n'
        print(output)
