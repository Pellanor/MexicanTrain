from random import shuffle

from src.GameState import GameState, draw_domino
from src.Player import Player
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
        bot_game_state = BotGameState(self.game_state, player)
        moves = player.bot.take_turn(bot_game_state)
        if len(moves) == 0:
            valid_moves = bot_game_state.get_all_valid_moves()
            if len(valid_moves) > 0:
                shuffle(valid_moves)
                self.do_move(player, valid_moves.pop(0))
            else:
                domino = draw_domino(self.game_state, player)
                if domino:
                    bot_game_state.draw_domino(len(player.dominoes) - 1, domino)
                    moves = player.bot.draw_tile(bot_game_state)
                    if len(moves) > 0:
                        self.do_move(player, moves.pop(0))
                else:
                    player.can_play = False
                    player.turn += 1
                    return
        else:
            self.do_move(player, moves.pop(0))
        player.turn += 1
        player.can_play = True

    def do_move(self, player: Player, move: BotMove):
        if player.dominoes.count(move.domino.value) == 0:
            raise RuntimeError("Cannot add Domino that player doesn't have!")
        if self.game_state.played.count(move.domino.value)> 0:
            raise RuntimeError("Cannot play a domino that has already been played!")
        train = self.game_state.trains[move.train.identity.train_id]
        domino = player.dominoes.pop(move.domino.domino_id)
        return train.add_domino(domino, player)

    def check_for_victory(self):
        player = self.game_state.current_player
        if len(player.dominoes) == 0:
            self.game_state.round_over = True
            self.game_state.round_winner = player
            player.victories += 1
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
