from chess import rules

def location_str(idx):
    return file_str(idx) + rank_str(idx)


def file_str(idx):
    return ('a', 'b', 'c', 'd', 'e', 'f', 'g')[idx[1]]


def rank_str(idx):
    return str(idx[0] + 1)


class Move(object):
    def __init__(self, start, end, algebraic):
        self.start = start
        self.end = end
        self.algebraic = algebraic

    @classmethod
    def on_board(cls, start, end, board):
        """
        Calculates the algebraic notation for a move on a board.
        """
        p = board[start]
        if p is None:
            return cls(start, end, "invalid")
        p_char = p.piece
        capture = ""
        if board[end] is not None:
            if p_char == "p":
                p_char = file_str(start)
            capture = "x"
        elif p_char == "p":
            p_char = ""
        end_str = location_str(end)
        if p_char != "p":
            disambig_from = []
            for loc in board.find(p):
                if loc == start:
                    continue
                if rules.move_is_valid(board, Move(loc, end, None)):
                    disambig_from.append(loc)
            ranks = [x[0] for x in disambig_from]
            files = [x[1] for x in disambig_from]
            if not disambig_from:
                disambig = ""
            # Check if all files are distinct
            elif start[1] not in files:
                disambig = file_str(start)
            elif start[0] not in ranks:
                disambig = rank_str(start)
            else:
                disambig = location_str(start)
        else:
            disambig = ""
        return cls(start, end, p_char + disambig + capture + end_str)

    @property
    def start_rank(self):
        return self.start[0]

    @property
    def end_rank(self):
        return self.end[0]

    @property
    def start_file(self):
        return self.start[1]

    @property
    def end_file(self):
        return self.end[1]

    def __str__(self):
        return self.algebraic
    __repr__ = __str__
