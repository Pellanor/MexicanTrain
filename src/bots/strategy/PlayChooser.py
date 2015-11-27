import abc

from src.bots.state import BotGameState


class PlayChooser:
    @abc.abstractmethod
    def choose_plays(self, game_state: BotGameState, plays):
        return

    @staticmethod
    def get_all_trains_for_plays(plays, trains):
        return [[train for train in trains if train.requires in play.starts_required] for play in plays]

    @staticmethod
    def get_results(chosen_plays, plays):
        if len(chosen_plays) > 0:
            return chosen_plays
        return plays

