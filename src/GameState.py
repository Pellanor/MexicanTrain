from random import shuffle

from src.Domino import Domino
from src.Player import Player
from src.Train import Train
from src.bots.BotFactory import get_long_bot, get_random_bot, get_fat_bot


class GameState:
    def __init__(self, player_count: int):
        self.trains = []
        self.players = []
        self.played = []
        self.played_count = {i: 0 for i in range(13)}
        self.dominoes = []
        self.round_over = False
        self.round_winner = None
        for i in range(player_count):
            if i == 0:
                self.players.append(Player(i, get_fat_bot()))
            elif i == 1:
                self.players.append(Player(i, get_long_bot()))
            else:
                self.players.append(Player(i, get_random_bot()))

        self.current_player = None

    def deal(self):
        self.dominoes = []
        for x in range(13):
            for y in range(x, 13):
                self.dominoes.append(Domino(x, y))

        shuffle(self.dominoes)

        for count in range(starting_dominoes_count(len(self.players))):
            for player in self.players:
                draw_domino(self, player)

    def clean_up_after_round(self):
        self.round_winner = None
        self.round_over = False
        self.trains = []
        self.played = []

    def start_round(self, round_number: int):
        self.deal()
        starting_domino = Domino(round_number, round_number)
        self.current_player = self.get_starting_player(starting_domino)

        for train_id, player in enumerate(self.players):
            self.trains.append(Train(train_id, round_number, player))
            player.bot.new_round(round_number)
        self.trains.append(Train(len(self.trains), round_number, None))

    def get_starting_player(self, starting_domino: Domino):
        starting_player = None
        for player in self.players:
            if player.dominoes.count(starting_domino) > 0:
                player.dominoes.remove(starting_domino)
                draw_domino(self, player)
                starting_player = player
        while starting_player is None:
            for player in self.players:
                if len(self.dominoes) > 0:
                    if draw_domino_and_check_for_start(self, player, starting_domino):
                        starting_player = player
        self.played_count[starting_domino.left] += 1
        self.played.append(starting_domino)
        return starting_player

    def next_player(self):
        self.current_player = self.players[(self.current_player.identity.id + 1) % len(self.players)]


def starting_dominoes_count(player_count: int):
    if 2 <= player_count <= 4:
        return 15
    elif 5 <= player_count <= 6:
        return 12
    elif 7 <= player_count <= 8:
        return 10
    else:
        return False


def draw_domino(game_state: GameState, player: Player):
    if len(game_state.dominoes) == 0:
        return False
    domino = game_state.dominoes.pop()
    player.give_domino(domino)
    return domino


def draw_domino_and_check_for_start(game_state: GameState, player: Player, starting_domino: Domino):
    if len(game_state.dominoes) == 0:
        raise RuntimeError(
            'Ran out of dominoes while trying to find the starting player. Did we miss the starting tile? ' +
            str(starting_domino))
    d = game_state.dominoes.pop()
    if d == starting_domino:
        if len(game_state.dominoes) > 0:
            player.give_domino(game_state.dominoes.pop())
        return True

    player.dominoes.append(d)
    return False


def place_domino(game_state: GameState, train: Train, domino: Domino, player: Player):
    if train.add_domino(domino, player):
        player.dominoes.remove(domino)
        game_state.played_count[domino.left] += 1
        if not domino.is_double:
            game_state.played_count[domino.right] += 1
        game_state.played.append(domino)
