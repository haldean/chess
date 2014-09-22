import copy


class Piece(object):
    def __init__(self, piece, color):
        assert piece in ('p', 'R', 'B', 'N', 'Q', 'K')
        assert color in ('w', 'b')
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
        return self.color == other.color and self.piece == other.piece

    def __str__(self):
        return self.color + self.piece
    __repr__ = __str__


class Board(object):
    def __init__(self, board=None):
        p = Piece
        if board is not None:
            self._board = board
            return
        self._board = [
            [p('R', 'w'), p('N', 'w'), p('B', 'w'), p('K', 'w'), p('Q', 'w'), p('B', 'w'), p('N', 'w'), p('R', 'w')],
            [p('p', 'w') for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [p('p', 'b') for _ in range(8)],
            [p('R', 'b'), p('N', 'b'), p('B', 'b'), p('K', 'b'), p('Q', 'b'), p('B', 'b'), p('N', 'b'), p('R', 'b')],
        ]

    @classmethod
    def parse(cls, instr):
        board = [[Piece.parse(pstr) for pstr in line.strip().split()]
                 for line in reversed(instr.strip().split("\n"))]
        return cls(board)

    def apply(self, move):
        board = copy.deepcopy(self._board)
        board[move.end[0]][move.end[1]] = self[move.start]
        board[move.start[0]][move.start[1]] = None
        return self.__class__(board)

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
