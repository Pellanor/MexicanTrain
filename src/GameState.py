from random import shuffle

from src.Domino import Domino
from src.GameSystem import GameSystem
from src.Player import Player
from src.Train import Train
from src.bots.RandomBot import RandomBot


class GameState:
    def __init__(self, player_count):
        self.trains = []
        self.players = []
        self.played = []
        self.play_count = {i: 0 for i in range(13)}
        self.dominoes = []
        self.round_over = False
        for i in range(player_count):
            self.players.append(Player(i, RandomBot()))

        self.current_player = None

    def deal(self):
        self.dominoes = []
        for x in range(13):
            for y in range(13):
                self.dominoes.append(Domino(x, y))
        shuffle(self.dominoes)

        for count in range(starting_dominoes_count(len(self.players))):
            for player in self.players:
                GameSystem.draw_domino(self, player)

    def start_round(self, round_number):
        self.deal()
        starting_domino = Domino(round_number, round_number)
        self.current_player = self.get_starting_player(starting_domino)
        self.trains = []

        for train_id, player in enumerate(self.players):
            self.trains.append(Train(train_id, round_number, player))
        self.trains.append(Train(len(self.trains), round_number, None))

    def get_starting_player(self, starting_domino):
        starting_player = None
        for player in self.players:
            if player.dominoes.count(starting_domino) > 0:
                player.dominoes.remove(starting_domino)
                GameSystem.draw_domino(self, player)
                starting_player = player
        while starting_player is None:
            for player in self.players:
                if len(self.dominoes) > 0:
                    if GameSystem.draw_domino_and_check_for_start(self, player, starting_domino):
                        starting_player = player

        self.played.append(starting_domino)
        return starting_player


def starting_dominoes_count(player_count):
    if 2 <= player_count <= 4:
        return 15
    elif 5 <= player_count <= 6:
        return 12
    elif 7 <= player_count <= 8:
        return 10
    else:
        return False
