from src.bots.FatBot import FatBot
from src.bots.LongBot import LongBot
from src.bots.MoveBot import MoveBot
from src.bots.strategy.Priority import Priority
from src.bots.strategy.priorities.PreferDemandSatisfaction import PreferDemandSatisfaction
from src.bots.strategy.priorities.PreferLeastPlayed import PreferLeastPlayed
from src.bots.strategy.priorities.PreferMakePrivate import PreferMakePrivate
from src.bots.strategy.priorities.PreferMexican import PreferMexican
from src.bots.strategy.priorities.PreferMinimizeScore import PreferMinimizeScore
from src.bots.strategy.priorities.PreferMostTiles import PreferMostTiles
from src.bots.strategy.priorities.PreferOwn import PreferOwn
from src.bots.strategy.priorities.PreferRandom import PreferRandom

"""
A Collection of functions for creating bots.
"""


def get_random_bot():
    """
    :return: A bot which returns a random move.
    """
    return MoveBot()


def get_long_bot():
    """
    :return: A bot which plays the longest possible path on the first turn.
    """
    return LongBot()


def get_fat_bot():
    """
    :return: A bot which plays the most tiles possible on the first turn.
    """
    return FatBot()


def get_smart_bot():
    """
    :return: A bot which plays the most tiles possible on the first turn.
        It will also try to be at least a little intelligent when choosing between moves.
    """
    priority_chain = [PreferMakePrivate(), PreferMexican(), PreferOwn(), PreferMostTiles(), PreferLeastPlayed(),
                      PreferMinimizeScore(), PreferDemandSatisfaction(), PreferRandom()]
    return FatBot(Priority(priority_chain))


def get_smart_move_bot():
    """
    :return: A bot which tries to be at least a little intelligent when choosing between moves.
    """
    priority_chain = [PreferMakePrivate(), PreferMexican(), PreferOwn(), PreferMostTiles(), PreferLeastPlayed(),
                      PreferMinimizeScore(), PreferDemandSatisfaction(), PreferRandom()]
    return MoveBot(Priority(priority_chain))


def get_bot(i):
    """
    Function to be used in loops when populating a game with bots.
    :param i: index to choose
    :return: A bot based on the index.
    """
    return {
        0: get_random_bot(),
        1: get_long_bot(),
        2: get_fat_bot(),
        3: get_smart_bot(),
        4: get_smart_move_bot()
    }.get(i, get_random_bot())
