import chess
import eco

class PossibleOpening(eco.Opening):
    def __init__(self, code, name, moves, summary, next_move):
        eco.Opening.__init__(self, code, name, summary, moves)
        self.next_move = next_move

    @classmethod
    def in_game(cls, game, opening):
        next_move = eco.eco_to_move(
            game.current_board, opening.moves[len(game.moves)])
        if game.to_play == chess.white:
            next_algebraic = "%d.%s" % (
                len(game.moves) // 2 + 1, next_move.algebraic)
        else:
            next_algebraic = "...%s" % next_move.algebraic
        return cls(
            opening.code, opening.name, opening.moves, opening.summary,
            next_algebraic)

def opening_stats(game, eco_data):
    if not game.moves:
        return None, []
    openings = sorted(eco.match(game, eco_data))
    if not openings:
        return None, []
    if len(openings) == 1:
        return openings[0], []
    potentials = filter(
            lambda o: len(o.moves) == len(game.moves) + 1, openings[1:])
    potentials = map(lambda o: PossibleOpening.in_game(game, o), potentials)
    if eco.is_exact_match(game, openings[0]):
        return openings[0], potentials
    return None, potentials
