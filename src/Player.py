class Player:
    def __init__(self, player_id, bot):
        self.dominoes = []
        self.player_id = player_id
        self.turn = 0
        self.victories = 0
        self.score = 0
        self.bot = bot

    def __eq__(self, other):
        return other is not None and self.player_id == other.player_id

    def give_domino(self, domino):
        self.dominoes.append(domino)

    def end_round(self, victor):
        if victor:
            self.victories += 1
        self.score += self.calc_score()

    def calc_score(self):
        score = 0
        for domino in self.dominoes:
            score += domino.left
            score += domino.right
        return score
