import chess

_material_value = {
    chess.pawn: 1,
    chess.rook: 5,
    chess.knight: 3,
    chess.bishop: 3,
    chess.queen: 9,
    chess.king: 0,
}

def material_values(game):
    black_material = 0
    white_material = 0
    for _, _, p in game.current_board:
        if p.color == chess.white:
            white_material += _material_value[p.piece]
        if p.color == chess.black:
            black_material += _material_value[p.piece]
    return white_material, black_material
