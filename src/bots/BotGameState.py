from copy import copy


class BotGameState:
    def __init__(self, game, player):
        self.all_trains = []
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
            self.all_trains.append(bot_train)
        self.dominoes_for_number = {i: [] for i in range(13)}
        self.dominoes = []
        for domino_id, domino in enumerate(player.dominoes):
            bd = BotDomino(domino_id, domino)
            self.dominoes.append(bd)
            self.dominoes_for_number[domino.left].append(bd)
            self.dominoes_for_number[domino.right].append(bd)
        self.played_count = game.played_count
        self.moves = []

    def get_unplayed_count(self, number):
        return 13 - self.played_count[number]

    def place_domino(self, bot_domino, bot_train):
        self.make_move(BotMove(bot_domino, bot_train))

    def make_move(self, bot_move):
        self.moves.append(bot_move)
        bot_move.bot_train.requires = bot_move.bot_domino.value.get_other_number(bot_move.bot_train.requires)

    def get_all_valid_moves(self):
        valid_moves = set()
        # Check if any train demands satisfaction
        for bot_train in self.playable_trains:
            if bot_train.demands_satisfaction:
                for bot_domino in self.dominoes_for_number[bot_train.requires]:
                    valid_moves.add(BotMove(bot_domino, bot_train))
                # Only one train can demand satisfaction at a time, no other moves are possible
                return valid_moves
        # Satisfaction not required. Add all possible moves.
        for bot_train in self.playable_trains:
            for bot_domino in self.dominoes_for_number[bot_train.requires]:
                valid_moves.add(BotMove(bot_domino, bot_train))
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
        return isinstance(other, self.__class__) and self.train_id == other.train_id

    def __hash__(self):
        return hash(self.train_id)


class BotPlayer:
    def __init__(self, player, bot_train):
        self.player_id = player.player_id
        self.tile_count = len(player.dominoes)
        self.train = bot_train

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.player_id == other.player_id


class BotDomino:
    def __init__(self, domino_id, domino):
        self.domino_id = domino_id
        self.value = domino

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value

    def __hash__(self):
        return hash(self.value)

class BotMove:
    def __init__(self, bot_domino, bot_train):
        self.domino_id = bot_domino.domino_id
        self.train_id = bot_train.train_id
        self.bot_domino = bot_domino
        self.bot_train = bot_train

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.bot_domino == other.bot_domino and self.bot_train == other.bot_train

    def __hash__(self):
        return hash(self.bot_domino) ^ hash(self.bot_train)