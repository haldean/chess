import chess

def game_to_eco_moves(game):
    eco_moves = []
    for move in game.moves:
        eco_move = chess.location_str(move.start) + chess.location_str(move.end)
        eco_moves.append(eco_move)
    return eco_moves

def is_exact_match(game, eco_move):
    game_moves = game_to_eco_moves(game)
    if len(game_moves) < len(eco_move.moves):
        return False
    for g, m in zip(game_moves, eco_move.moves):
        if g != m:
            return False
    return True

def match(game, eco_tree):
    eco_moves = game_to_eco_moves(game)
    while eco_moves and eco_moves[0] in eco_tree.children:
        eco_tree = eco_tree.children[eco_moves[0]]
        eco_moves = eco_moves[1:]
    if eco_moves:
        # We only matched a sublist of the game's moves; we've been locked into
        # an opening at this point. The means of progression aren't available
        # any more; only return moves at this level.
        return eco_tree.moves
    # Even with all of the moves in the game so far, we haven't matched
    # everything. Return all of the openings reachable from the current game
    # state.
    return eco_tree.all_submoves()
