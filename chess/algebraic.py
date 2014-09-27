"""
Parse algebraic notation.
"""

from chess import board
from chess import move
from chess.const import *

def parse_algebraic(b, color, notation):
    algebraic = notation
    # Special-case castles, these have nothing to do with "standard" algebraic
    # notation.
    if notation in ("0-0", "O-O", "0-0-0", "O-O-O"):
        if color == black:
            rank = 7
        else:
            rank = 0
        if notation in ("0-0-0", "O-O-O"):
            end_file = 5
            side = queenside
        else:
            end_file = 1
            side = kingside
        return move.Move(
            (rank, 3), (rank, end_file), algebraic, (color, side))
    # Find the piece that's moving
    if notation[0] in pieces:
        piece = notation[0]
        notation = notation[1:]
    else:
        piece = pawn
    # Strip off the checking information, we don't need that to figure out where
    # we moved to.
    notation = notation.rstrip('#').rstrip('+')
    end_loc = notation[-2:]
    end_file = move.file_from_str(end_loc[0])
    end_rank = move.rank_from_str(end_loc[1])
    is_capture = "x" in notation
    # If the piece is a pawn, the notation is a bit, uh, special.
    if piece == pawn:
        file = move.file_from_str(notation[0])
        file_pieces = b.file(file)
        if not is_capture:
            end_rank = move.rank_from_str(notation[1])
            if color == white:
                if end_rank == 3:
                    start_ranks = [2, 1]
                else:
                    start_ranks = [end_rank - 1]
            else:
                if end_rank == 4:
                    start_ranks = [5, 6]
                else:
                    start_ranks = [end_rank + 1]
            for r in start_ranks:
                piece = file_pieces[r]
                if piece is None:
                    continue
                # If there's a piece between our white pawn and the target,
                # this is an invalid move.
                if piece.color != color or piece.piece != pawn:
                    raise ValueError("No %s pawns can move to %s" %
                                     (color_names[color], notation))
                return move.Move(
                    (r, file), (end_rank, file), algebraic, None)
            raise ValueError("No %s pawns can move to %s" %
                             (color_names[color], notation))
        # Okay, so it's a capture. This is actually a lot easier.
        if color == white:
            rank = end_rank - 1
        else:
            rank = end_rank + 1
        if not b[rank, file]:
            raise ValueError("No %s pawns can attack %s" %
                             (color_names[color], end_loc))
        return move.Move(
            (rank, file), (end_rank, end_file), algebraic, None)
    if is_capture:
        disambig = notation[:notation.find("x")]
    else:
        disambig = notation[:-2]
    disambig_rank = None
    disambig_file = None
    if len(disambig) == 1:
        if disambig in files:
            disambig_file = move.file_from_str(disambig)
        elif disambig in ranks:
            disambig_rank = move.rank_from_str(disambig)
        else:
            raise ValueError("Unknown disambiguation %s in notation %s" %
                             (disambig, algebraic))
    elif len(disambig) == 2:
        disambig_file = move.file_from_str(disambig[0])
        disambig_rank = move.rank_from_str(disambig[1])
    elif len(disambig) > 2:
        raise ValueError("Unknown disambiguation %s in notation %s" %
                         (disambig, algebraic))
    for sr, sf, p in move.pieces_with_access(b, (end_rank, end_file)):
        if p.piece != piece or p.color != color:
            continue
        if disambig_rank is not None and sr != disambig_rank:
            continue
        if disambig_file is not None and sf != disambig_file:
            continue
        return move.Move((sr, sf), (end_rank, end_file), algebraic, None)
    raise ValueError("No %s %s (with disambig %s) can attack %s" %
                     (color_names[color], piece_names[piece], disambig, end_loc))
