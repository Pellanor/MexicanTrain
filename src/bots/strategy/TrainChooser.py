import abc

from src.bots.state import BotGameState


class TrainChooser:
    @abc.abstractmethod
    def choose_trains(self, game_state: BotGameState, trains):
        return

    @staticmethod
    def get_results(chosen_trains, trains):
        if len(chosen_trains) > 0:
            return chosen_trains
        return trains
