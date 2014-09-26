"""
Parse algebraic notation.
"""

from chess import board
from chess import move
from chess.const import *

def parse_algebraic(b, color, notation):
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
        file = notation[0]
        file_pieces = b.file(file)
        is_capture = "x" in notation
    print notation
