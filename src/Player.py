class Player:
    def __init__(self, player_id):
        self.dominoes = []
        self.playerId = player_id
        self.turn = 0
        self.victories = 0
        self.score = 0

    def __eq__(self, other):
        return other is not None and self.playerId == other.playerId

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
