from random import shuffle
from src.Domino import Domino
from src.Player import Player
from src.Train import Train


class GameState:
    """
    Class that tracks all the stuff for the current game.
    """

    def __init__(self, player_count: int):
        """
        Create a new GameState for a game containing the specified number of players.
        :param player_count: number of players.
        """
        self.trains = []
        self.players = []
        self.played = []
        self.played_count = {i: 0 for i in range(13)}
        self.dominoes = []
        self.round_over = False
        self.round_winner = None
        for i in range(player_count):
            from src.bots.BotFactory import get_bot
            self.players.append(Player(i, get_bot(i)))

        self.current_player = None

    def deal(self):
        """
        Deal out dominoes for all players for the current round,
        """
        self.dominoes = []
        for x in range(13):
            for y in range(x, 13):
                self.dominoes.append(Domino(x, y))

        shuffle(self.dominoes)

        for count in range(starting_dominoes_count(len(self.players))):
            for player in self.players:
                self.draw_domino(player)

    def clean_up_after_round(self):
        """
        Do any necessary end of round clean up.
        """
        self.round_winner = None
        self.round_over = False
        self.trains = []
        self.played = []

    def start_round(self, round_number: int):
        """
        Start a new round.
        :param round_number: The round number ot start.
        """
        self.deal()
        starting_domino = Domino(round_number, round_number)
        self.current_player = self.get_starting_player(starting_domino)

        for train_id, player in enumerate(self.players):
            self.trains.append(Train(train_id, round_number, player))
            player.bot.new_round(round_number)
        self.trains.append(Train(len(self.trains), round_number, None))

    def get_starting_player(self, starting_domino: Domino) -> Player:
        """
        For the current round, determine who goes first.
        :param starting_domino: The domino required for the first player.
        :return: The Player who will go first.
        """
        starting_player = None
        for player in self.players:
            if player.dominoes.count(starting_domino) > 0:
                player.dominoes.remove(starting_domino)
                self.draw_domino(player)
                starting_player = player
        while starting_player is None:
            for player in self.players:
                if len(self.dominoes) > 0:
                    if self.draw_domino_and_check_for_start(player, starting_domino):
                        starting_player = player
        self.played_count[starting_domino.left] += 1
        self.played.append(starting_domino)
        return starting_player

    def next_player(self):
        """
        Set the current player to be whoever comes after the current player.
        """
        self.current_player = self.players[(self.current_player.identity.id + 1) % len(self.players)]

    def draw_domino(self, player: Player):
        """
        Draw a domino for the specified player.
        :param player: the player to add the domino to.
        :return: the domino that was drawn and given to the player.
        """
        if len(self.dominoes) == 0:
            return False
        domino = self.dominoes.pop()
        player.give_domino(domino)
        return domino

    def place_domino(self, train: Train, domino: Domino, player: Player):
        """
        Place a domino on a Train.
        :param train: The Train to add the Domino to.
        :param domino: The Domino to add.
        :param player: The Player who is placing the domino.
        """
        if train.add_domino(domino, player):
            player.dominoes.remove(domino)
            self.played_count[domino.left] += 1
            if not domino.is_double:
                self.played_count[domino.right] += 1
            self.played.append(domino)

    def draw_domino_and_check_for_start(self, player: Player, starting_domino: Domino) -> bool:
        """
        Helper function when determine the first player.
        Draws a domino for tha player, then checks to see if it is the required domino for going first.
        :param player: the player to add the domino to.
        :param starting_domino: the required starting Domino
        :return: True if the starting_domino was drawn.
        """
        if len(self.dominoes) == 0:
            raise RuntimeError(
                'Ran out of dominoes while trying to find the starting player. Did we miss the starting tile? ' +
                str(starting_domino))
        d = self.dominoes.pop()
        if d == starting_domino:
            if len(self.dominoes) > 0:
                player.give_domino(self.dominoes.pop())
            return True

        player.dominoes.append(d)
        return False


def starting_dominoes_count(player_count: int) -> int:
    """
    Get the number of dominoes that each player starts with each round.
    :param player_count: players in the current game.
    :return: number of starting dominoes.
    """
    if 2 <= player_count <= 4:
        return 15
    elif 5 <= player_count <= 6:
        return 12
    elif 7 <= player_count <= 8:
        return 10
    else:
        return False
