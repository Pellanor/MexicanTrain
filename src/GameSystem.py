class GameSystem:
    @staticmethod
    def draw_domino(game_state, player):
        if len(game_state.dominoes) == 0:
            return False
        player.give_domino(game_state.dominoes.pop())
        return True

    @staticmethod
    def draw_domino_and_check_for_start(game_state, player, starting_domino):
        if len(game_state.dominoes) == 0:
            raise RuntimeError(
                'Ran out of dominoes while trying to find the starting player. Did we miss the starting tile? ' +
                str(starting_domino))
        d = game_state.dominoes.pop()
        if d == starting_domino:
            if len(game_state.dominoes) > 0:
                player.give_domino(game_state.dominoes.pop())
            return True

        player.dominoes.append(d)
        return False

    @staticmethod
    def place_domino(game_state, train, domino, player):
        if train.add_domino(domino, player):
            player.dominoes.remove(domino)
            game_state.played_count[domino.left] += 1
            game_state.played_count[domino.right] += 1
            game_state.played.append(domino)
