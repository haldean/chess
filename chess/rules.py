def _any_between(board, move):
    for r in range(move.start_rank, move.end_rank + 1):
        for f in range(move.start_file, move.end_file + 1):
            if (r, f) == move.start or (r, f) == move.end:
                continue
            if board[r, f] is not None:
                return True
    return False

def _pawn_move_is_valid(move, start_p, end_p):
    if end_p is None:
        if move.start_file != move.end_file:
            return False
        if start_p.color == 'w':
            if move.start_rank == 1:
                if move.end_rank not in (2, 3):
                    return False
            elif move.end_rank - move.start_rank != 1:
                return False
        else:
            if move.start_rank == 7:
                if move.end_rank not in (6, 5):
                    return False
            elif move.end_rank - move.start_rank != -1:
                return False
    else:
        if abs(move.start_file - move.end_file) != 1:
            return False
        if start_p.color == 'w':
            if move.end_rank - move.start_rank != 1:
                return False
        else:
            if move.end_rank - move.start_rank != -1:
                return False
    return True

def _rook_move_is_valid(move):
    return move.start_file == move.end_file or move.start_rank == move.end_rank

def move_is_valid(board, move):
    start_p = board[move.start]
    if start_p is None:
        return False
    end_p = board[move.end]
    if end_p is not None and start_p.color == end_p.color:
        return False
    if start_p.piece == 'p':
        if _any_between(board, move):
            return False
        return _pawn_move_is_valid(move, start_p, end_p)
    if start_p.piece == 'R':
        if _any_between(board, move):
            return False
        return _rook_move_is_valid(move)
    raise Exception("No rules for piece " + start_p.piece)
