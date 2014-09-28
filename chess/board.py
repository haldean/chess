import copy

from chess.const import *

class Piece(object):
    def __init__(self, color, piece):
        if color not in colors:
            raise ValueError("Invalid color '%s'" % color)
        if piece not in pieces:
            raise ValueError("Invalid piece '%s'" % piece)
        self.piece = piece
        self.color = color

    @classmethod
    def parse(cls, instr):
        instr = instr.strip()
        assert len(instr) == 2
        if instr in ("__", "  "):
            return None
        return cls(instr[0], instr[1])

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
        return cls.parse("""
        bR bN bB bQ bK bB bN bR
        bp bp bp bp bp bp bp bp
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        wp wp wp wp wp wp wp wp
        wR wN wB wQ wK wB wN wR
        """)

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
                board[rank][5] = board[rank][7]
                board[rank][7] = None
            else:
                board[rank][3] = board[rank][0]
                board[rank][0] = None
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

    def rank(self, r):
        return list(self._board[r])

    def file(self, f):
        res = []
        for r in range(8):
            res.append(self[r, f])
        return res

    def __setitem__(self, idx, val):
        self._board[idx[0]][idx[1]] = val

    def __getitem__(self, idx):
        try:
            return self._board[idx[0]][idx[1]]
        except TypeError:
            raise TypeError(
                "Indeces should be (rank, file) tuples, got '%s'" % (idx,))

    def __iter__(self):
        return _BoardIterator(self)

    def __str__(self):
        def _str(piece):
            if piece is None:
                return "__"
            return str(piece)
        return "\n".join("  ".join(_str(p) for p in rank)
            for rank in reversed(self._board))
    __repr__ = __str__

class _BoardIterator(object):
    def __init__(self, board):
        self.board = board
        self.next_loc = (0, 0)

    def next(self):
        while self.next_loc[0] < 8:
            while self.next_loc[1] < 8:
                val = self.board[self.next_loc]
                val_loc = self.next_loc
                self.next_loc = (self.next_loc[0], self.next_loc[1] + 1)
                if val is not None:
                    return val_loc[0], val_loc[1], val
            self.next_loc = (self.next_loc[0] + 1, 0)
        raise StopIteration()
