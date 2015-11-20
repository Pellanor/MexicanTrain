from copy import copy

import collections

Move = collections.namedtuple('Move', ['domino_id', 'train_id'])


class BotGameState:
    def __init__(self, game, player):
        self.playable_trains = []
        self.other_trains = []
        for train_id, train in enumerate(game.trains):
            bot_train = BotTrain(train_id, train, player)
            if bot_train.owned:
                self.my_train = bot_train
            if bot_train.can_add:
                self.playable_trains.append(bot_train)
            else:
                self.other_trains.append(bot_train)
        self.dominoes_for_number = {i: [] for i in range(13)}
        self.dominoes = []
        for domino_id, domino in enumerate(player.dominoes):
            bd = BotDomino(domino_id, domino)
            self.dominoes.append(bd)
            self.dominoes_for_number[domino.left].append(bd)
            self.dominoes_for_number[domino.right].append(bd)
        self.played_count = game.play_count
        self.moves = []

    def get_unplayed_count(self, number):
        return 13 - self.played_count[number]

    def place_domino(self, bot_domino, bot_train):
        self.moves.append(Move(bot_domino.domino_id, bot_train.train_id))
        bot_train.requires = bot_domino.value.other_number(bot_train.requires)

    @property
    def get_all_valid_moves(self):
        valid_moves = set()

        # Check if any train demands satisfaction
        for bot_train in self.playable_trains:
            if bot_train.demands_satisfaction:
                for bot_domino in self.dominoes_for_number[bot_train.requires]:
                    valid_moves.add(Move(bot_domino.domino_id, bot_train.train_id))
                # Only one train can demand satisfaction at a time, no other moves are possible
                return valid_moves

        for bot_train in self.playable_trains:
            for bot_domino in self.dominoes_for_number[bot_train.requires]:
                valid_moves.add(Move(bot_domino.domino_id, bot_train.train_id))
        return valid_moves


class BotTrain:
    def __init__(self, train_id, train, player):
        self.train_id = train_id
        self.owned = train.owner == player
        self.mexican = train.owner is None
        if not self.mexican:
            self.owner_id = train.owner.player_id
        else:
            self.owner_id = None
        self.can_add = train.can_player_add(player)
        self.cars = copy(train.cars)
        self.original_requires = self.requires = train.requires
        self.demands_satisfaction = train.demands_satisfaction

    def __eq__(self, other):
        return self.train_id == other.train_id


class BotPlayer:
    def __init__(self, player, bot_train):
        self.player_id = player.player_id
        self.tile_count = len(player.dominoes)
        self.train = bot_train

    def __eq__(self, other):
        return self.player_id == other.player_id


class BotDomino:
    def __init__(self, domino_id, domino):
        self.domino_id = domino_id
        self.value = domino

    def __eq__(self, other):
        return self.value == other.value
