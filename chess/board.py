import copy

from chess.const import *

class Piece(object):
    def __init__(self, piece, color):
        assert piece in pieces
        assert color in colors
        self.piece = piece
        self.color = color

    @classmethod
    def parse(cls, instr):
        instr = instr.strip()
        assert len(instr) == 2
        if instr in ("__", "  "):
            return None
        return cls(instr[1], instr[0])

    def __eq__(self, other):
        if other is None:
            return False
        return self.color == other.color and self.piece == other.piece

    def __str__(self):
        return self.color + self.piece
    __repr__ = __str__


class Board(object):
    def __init__(
            self, board, open_castles, last_move, last_board,
            en_passantable):
        self._open_castles = open_castles
        self._board = board
        self.last_move = last_move
        self.last_board = last_board
        self.en_passantable = en_passantable

    @classmethod
    def new(cls):
        p = Piece
        board = [
            [p('R', 'w'), p('N', 'w'), p('B', 'w'), p('K', 'w'),
                p('Q', 'w'), p('B', 'w'), p('N', 'w'), p('R', 'w')],
            [p('p', 'w') for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [p('p', 'b') for _ in range(8)],
            [p('R', 'b'), p('N', 'b'), p('B', 'b'), p('K', 'b'),
                p('Q', 'b'), p('B', 'b'), p('N', 'b'), p('R', 'b')],
        ]
        return cls(board, all_castles, None, None, None)

    @classmethod
    def parse(cls, instr):
        board = [[Piece.parse(pstr) for pstr in line.strip().split()]
                 for line in reversed(instr.strip().split("\n"))]
        return cls(board, all_castles, None, None, None)

    def can_castle(self, color, side):
        return (color, side) in self._open_castles

    def apply(self, move):
        board = copy.deepcopy(self._board)
        board[move.end_rank][move.end_file] = self[move.start]
        board[move.start_rank][move.start_file] = None
        open_castles = set(self._open_castles)
        if move.is_castle:
            # Remove this color's castles.
            for castle in self._open_castles:
                if castle[0] == move.castle[0]:
                    open_castles.remove(castle)
            # Move the corresponding rook too.
            if move.castle[0] == black:
                rank = 7
            else:
                rank = 0
            if move.castle[1] == kingside:
                board[rank][2] = board[rank][0]
                board[rank][0] = None
            else:
                board[rank][4] = board[rank][7]
                board[rank][7] = None
        en_passantable = None
        start_p = self[move.start]
        if start_p.piece == pawn:
            d_rank = abs(move.end_rank - move.start_rank)
            d_file = abs(move.end_file - move.start_file)
            # Assume that this move has already been validated, so a pawn move
            # by two is the first pawn development.
            if d_rank == 2:
                en_passantable = move.end
            elif d_rank == 1 and d_file == 1:
                end_p = self[move.end] 
                if end_p is None:
                    if start_p.color == black:
                        passing_rank = 2
                        en_passant_rank = 3
                    else:
                        passing_rank = 5
                        en_passant_rank = 4
                    if move.end_rank == passing_rank and move.end_file in self.en_passantable:
                        p_loc = (en_passant_rank, move.end[1])
                        board[p_loc[0]][p_loc[1]] = None
        return self.__class__(board, open_castles, move, self, en_passantable)

    def find(self, piece):
        for ri, rank in enumerate(self._board):
            for fi, p in enumerate(rank):
                if p and piece == p:
                    yield (ri, fi)

    def __getitem__(self, idx):
        return self._board[idx[0]][idx[1]]

    def __str__(self):
        def _str(piece):
            if piece is None:
                return "__"
            return str(piece)
        return "\n".join("  ".join(_str(p) for p in rank)
            for rank in reversed(self._board))
    __repr__ = __str__
