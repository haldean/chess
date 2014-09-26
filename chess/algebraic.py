"""
Parse algebraic notation.
"""

from chess import board
from chess import move
from chess.const import *

def parse_algebraic(b, color, notation):
    algebraic = notation
    # Find the piece that's moving
    if notation[0] in pieces:
        piece = notation[0]
        notation = notation[1:]
    else:
        piece = pawn
    # Strip off the checking information, we don't need that to figure out where
    # we moved to.
    notation = notation.rstrip('#').rstrip('+')
    # If the piece is a pawn, the notation is a bit, uh, special.
    if piece == pawn:
        file = move.file_from_str(notation[0])
        file_pieces = b.file(file)
        is_capture = "x" in notation
        if not is_capture:
            end_rank = move.rank_from_str(notation[1])
            if color == white:
                if end_rank == 3:
                    ranks = [2, 1]
                else:
                    ranks = [end_rank - 1]
            else:
                if end_rank == 4:
                    ranks = [5, 6]
                else:
                    ranks = [end_rank + 1]
            for r in ranks:
                piece = file_pieces[r]
                if piece is None:
                    continue
                # If there's a piece between our white pawn and the target,
                # this is an invalid move.
                if piece.color != color or piece.piece != pawn:
                    raise ValueError(
                        "No %s pawns can move to %s" % (color, notation))
                return move.Move(
                    (r, file), (end_rank, file), algebraic, None)
            raise ValueError("No %s pawns can move to %s" % (color, notation))
        # Okay, so it's a capture. This is actually a lot easier.
        end_loc = notation[-2:]
        end_file = move.file_from_str(end_loc[0])
        end_rank = move.rank_from_str(end_loc[1])
        if color == white:
            rank = end_rank - 1
        else:
            rank = end_rank + 1
        if not b[rank, file]:
            raise ValueError("No %s pawns can attack %s" % (color, end_loc))
        return move.Move(
            (rank, file), (end_rank, end_file), algebraic, None)
    print notation
