from src.bots.FatBot import FatBot
from src.bots.LongBot import LongBot
from src.bots.MoveBot import MoveBot
from src.bots.strategy.Priority import Priority
from src.bots.strategy.priorities.PreferDemandSatisfaction import PreferDemandSatisfaction
from src.bots.strategy.priorities.PreferLeastPlayed import PreferLeastPlayed
from src.bots.strategy.priorities.PreferMakePrivate import PreferMakePrivate
from src.bots.strategy.priorities.PreferMexican import PreferMexican
from src.bots.strategy.priorities.PreferMostTiles import PreferMostTiles
from src.bots.strategy.priorities.PreferOwn import PreferOwn
from src.bots.strategy.priorities.PreferRandom import PreferRandom


def get_random_bot():
    return MoveBot()


def get_long_bot():
    return LongBot()


def get_fat_bot():
    return FatBot()


def get_smart_bot():
    priority_chain = [PreferMakePrivate(), PreferMexican(), PreferOwn(), PreferMostTiles(), PreferLeastPlayed(),
                      PreferDemandSatisfaction(), PreferRandom()]
    return FatBot(Priority(priority_chain))


def get_smart_move_bot():
    priority_chain = [PreferMakePrivate(), PreferMexican(), PreferOwn(), PreferMostTiles(), PreferLeastPlayed(),
                      PreferDemandSatisfaction(), PreferRandom()]
    return MoveBot(Priority(priority_chain))


def get_bot(i):
    return {
        0: get_random_bot(),
        1: get_long_bot(),
        2: get_fat_bot(),
        3: get_smart_bot(),
        4: get_smart_move_bot()
    }.get(i, get_random_bot())
