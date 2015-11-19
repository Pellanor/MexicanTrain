from random import shuffle

from src.Domino import Domino
from src.Player import Player
from src.Train import Train
from src.bots.BotGameState import BotGameState
from src.bots.RandomBot import RandomBot


def starting_dominoes_count(player_count):
    if 2 <= player_count <= 4:
        return 15
    elif 5 <= player_count <= 6:
        return 12
    elif 7 <= player_count <= 8:
        return 10
    else:
        return False


class Game:
    def __init__(self, player_count):
        self.bots = []
        self.round_over = False
        self.trains = []
        self.players = []
        self.played = []
        for i in range(player_count):
            self.players.append(Player(i))
        for player in self.players:
            self.bots.append(RandomBot(BotGameState(self, player)))

        self.current_bot = None
        self.dominoes = []

    def deal(self):
        self.dominoes = []
        for x in range(13):
            for y in range(13):
                self.dominoes.append(Domino(x, y))
        shuffle(self.dominoes)

        for count in range(starting_dominoes_count(len(self.players))):
            for player in self.players:
                player.give_domino(self.draw())

    def start_round(self, round_number):
        self.deal()
        starting_domino = Domino(round_number, round_number)
        self.current_bot = self.get_starting_player(starting_domino)
        self.trains = []
        train_id = 0
        for player in self.players:
            t = Train(train_id, round_number, player)
            t.make_private()
            self.trains.append(t)
            train_id += 1
        self.trains.append(Train(train_id, round_number, None))

    def get_starting_player(self, starting_domino):
        starting_player = None
        for player in self.players:
            if player.dominoes.count(starting_domino) > 0:
                player.dominoes.remove(starting_domino)
                player.dominoes.append(self.draw())
                starting_player = player
        while starting_player is None:
            for player in self.players:
                if len(self.dominoes) > 0:
                    d = self.draw()
                    if d == starting_domino:
                        starting_player = player
                        player.give_domino(self.draw())
                    else:
                        player.dominoes.append(d)
        self.played.append(starting_domino)
        return starting_player

    def get_playable_trains(self, player):
        playable_trains = []
        for train in self.trains:
            if train.can_player_add(player):
                playable_trains.append(train)
        return playable_trains

    def draw(self):
        return self.dominoes.pop()

    def play(self):
        for cur_round in range(12, 0, -1):
            self.start_round(cur_round)
            while not self.round_over:
                self.take_turn()
                self.check_for_victory()
                self.next_player()

    def take_turn(self):
        player = self.current_bot
        if player.turn == 0:
            pass

    def check_for_victory(self):
        pass

    def next_player(self):
        self.current_bot = self.players[self.current_bot.playerId + 1 % len(self.players)]
