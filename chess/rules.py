from chess import board
from chess.const import *

def is_castle(b, start, end):
    start_p = b[start]
    if start_p is None or start_p.piece != 'K':
        return False
    color = start_p.color
    if color == white:
        rank = 0
    else:
        rank = 7
    if start[0] != rank or end[0] != rank:
        return False
    if end[1] == 1:
        if b.can_castle(color, kingside):
            for file in (3, 2, 1):
                if in_check(b, color, (rank, file)):
                    return False
            return (color, kingside)
    elif end[1] == 5:
        if b.can_castle(color, queenside):
            for file in (3, 4, 5):
                if in_check(b, color, (rank, file)):
                    return False
            return (color, queenside)
    return False


def in_check(b, color, position=None):
    """
    Returns true if the king would be in check if it were in the given position.
    If no position is given, the location of the king is pulled from the board.
    """
    if position is None:
        positions = list(b.find(board.Piece(color, king)))
        if len(positions) != 1:
            raise Exception("Board has %d %s kings" % (len(positions), color))
        position = positions[0]
    for rank in range(8):
        for file in range(8):
            if b[rank, file] is None:
                continue
            if b[rank, file].color == color:
                continue
            if _move_is_valid(b, (rank, file), position):
                return True
    return False


def _any_between(b, start, end):
    start_rank, start_file = start
    end_rank, end_file = end
    for r in range(start_rank, end_rank + 1):
        for f in range(start_file, end_file + 1):
            if (r, f) == start or (r, f) == end:
                continue
            if b[r, f] is not None:
                return True
    return False


def _pawn_move_is_valid(b, start, end):
    start_p = b[start]
    end_p = b[end]
    start_rank, start_file = start
    end_rank, end_file = end
    if end_p is None:
        if start_file != end_file:
            if b.en_passantable is not None:
                if b[b.en_passantable].color == start_p.color:
                    return False
                if start_p.color == white:
                    if end_rank == 5 and end_file == b.en_passantable[1]:
                        return True
                if start_p.color == black:
                    if end_rank == 2 and end_file == b.en_passantable[1]:
                        return True
            return False
        if start_p.color == white:
            if start_rank == 1:
                if end_rank not in (2, 3):
                    return False
            elif end_rank - start_rank != 1:
                return False
        else:
            if start_rank == 6:
                if end_rank not in (5, 4):
                    return False
            elif end_rank - start_rank != -1:
                return False
    else:
        if abs(start_file - end_file) != 1:
            return False
        if start_p.color == white:
            if end_rank - start_rank != 1:
                return False
        else:
            if end_rank - start_rank != -1:
                return False
    return True

def _rook_move_is_valid(start, end):
    start_rank, start_file = start
    end_rank, end_file = end
    return start_file == end_file or start_rank == end_rank

def _king_move_is_valid(b, start, end):
    if is_castle(b, start, end):
        return True
    start_rank, start_file = start
    end_rank, end_file = end
    return abs(start_rank - end_rank) < 1 and abs(start_file - end_file) < 1

def _knight_move_is_valid(start, end):
    start_rank, start_file = start
    end_rank, end_file = end
    d_rank = abs(start_rank - end_rank)
    d_file = abs(start_file - end_file)
    return (d_rank == 2 and d_file == 1) or (d_rank == 1 and d_file == 2)

def _bishop_move_is_valid(start, end):
    start_rank, start_file = start
    end_rank, end_file = end
    d_rank = abs(start_rank - end_rank)
    d_file = abs(start_file - end_file)
    return d_rank == d_file

def _queen_move_is_valid(start, end):
    return _bishop_move_is_valid(start, end) or _rook_move_is_valid(start, end)

def move_is_valid(b, move):
    return _move_is_valid(b, move.start, move.end)

def _move_is_valid(b, start, end):
    if not 0 <= start[0] <= 7 or not 0 <= start[1] <= 7:
        return False
    if not 0 <= end[0] <= 7 or not 0 <= end[1] <= 7:
        return False
    start_p = b[start]
    if start_p is None:
        return False
    end_p = b[end]
    if end_p is not None and start_p.color == end_p.color:
        return False
    if start_p.piece == pawn:
        if _any_between(b, start, end):
            return False
        return _pawn_move_is_valid(b, start, end)
    if start_p.piece == rook:
        if _any_between(b, start, end):
            return False
        return _rook_move_is_valid(start, end)
    if start_p.piece == king:
        if _any_between(b, start, end):
            return False
        return _king_move_is_valid(b, start, end)
    if start_p.piece == knight:
        return _knight_move_is_valid(start, end)
    if start_p.piece == bishop:
        if _any_between(b, start, end):
            return False
        return _bishop_move_is_valid(start, end)
    if start_p.piece == queen:
        if _any_between(b, start, end):
            return False
        return _queen_move_is_valid(start, end)
    raise NotImplementedError("No rules for piece " + start_p.piece)
