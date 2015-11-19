from copy import copy


class BotGameState:
    def __init__(self, game, player):
        self.__game = game
        self.__player = player

    def get_playable_train_ends(self):
        return [TrainEnd(train) for train in self.__game.trains if train.can_player_add(self.__player)]

    def get_all_trains_ends(self):
        return [TrainEnd(train) for train in self.__game.trains]

    def get_dominoes(self):
        return copy(self.__player.dominoes)

    def get_unplayed_count(self, number):
        unplayed = 13
        for domino in self.__game.played:
            if domino.contains(number):
                unplayed -= 1
        return unplayed

    def get_domino_id(self, domino):
        return self.__player.dominoes.index(domino)

    def place_domino(self, domino_id, train_id):
        if self.__player.can_place():
            domino = self.__player.dominoes[domino_id]
            if self.__game.trains[train_id].add_domino(domino):
                self.__player.placed += 1
                self.__player.dominoes.remove(domino)
                self.__game.played.append(domino)
                return True
        return False

    def end_turn(self):
        if self.__player.has_ended:
            return True
        if self.__player.placed == 0:
            if self.__player.has_drawn is False:
                self.__player.dominoes.append(self.__game.draw())
            else:
                for train in self.__game.trains:
                    if train.owner == self.__player:
                        train.make_public()


class TrainEnd:
    def __init__(self, train):
        self.__train = train

    def get_train_end(self):
        return self.__train.train_id, self.__train.requires

    def __str__(self):
        return str(self.__train.train_id) + ":" + str(self.__train.requires)
