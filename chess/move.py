import copy

from chess import board
from chess.const import *

def location_str(idx):
    return _file_str(idx) + _rank_str(idx)


def _file_str(idx):
    return ('a', 'b', 'c', 'd', 'e', 'f', 'g')[idx[1]]


def file_from_str(file):
    if file not in files:
        raise ValueError("Invalid file \"%s\"" % file)
    return ord(file) - ord('a')


def _rank_str(idx):
    return str(idx[0] + 1)


def rank_from_str(rank):
    if rank not in ranks:
        raise ValueError("Invalid rank \"%s\"" % rank)
    return int(rank) - 1


class Move(object):
    def __init__(self, start, end, algebraic, castle):
        self.start = start
        self.end = end
        self.algebraic = algebraic
        if self.algebraic is None:
            self.algebraic = "?"
        self.castle = castle

    @classmethod
    def on_board(cls, start, end, b):
        """
        Calculates the algebraic notation for a move on a board.
        """
        castle = is_castle(b, start, end)
        if castle:
            if castle[1] == kingside:
                return cls(start, end, "0-0", castle)
            else:
                return cls(start, end, "0-0-0", castle)
        p = b[start]
        if p is None:
            return cls(start, end, "invalid", None)
        p_char = p.piece
        capture = ""
        if b[end] is not None:
            if p_char == "p":
                p_char = _file_str(start)
            capture = "x"
        elif p_char == "p":
            p_char = ""
        end_str = location_str(end)
        if p_char != "p":
            disambig_from = []
            for loc in b.find(p):
                if loc == start:
                    continue
                if _move_is_valid(b, loc, end):
                    disambig_from.append(loc)
            ranks = [x[0] for x in disambig_from]
            files = [x[1] for x in disambig_from]
            if not disambig_from:
                disambig = ""
            # Check if all files are distinct
            elif start[1] not in files:
                disambig = _file_str(start)
            elif start[0] not in ranks:
                disambig = _rank_str(start)
            else:
                disambig = location_str(start)
        else:
            disambig = ""
        after_move = b.apply(cls(start, end, "test-check-move", None))
        if p.color == white:
            opposite_color = black
        else:
            opposite_color = white
        if in_checkmate(after_move, opposite_color):
            check_str = "#"
        elif in_check(after_move, opposite_color):
            check_str = "+"
        else:
            check_str = ""
        return cls(
            start, end,
            p_char + disambig + capture + end_str + check_str,
            None)

    def is_valid(self, b):
        return _move_is_valid(b, self.start, self.end)

    @property
    def is_castle(self):
        return self.castle is not None

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

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return (self.start == other.start and
                self.end == other.end and
                self.castle == other.castle)

    def __str__(self):
        return "%s [%s -> %s]" % (self.algebraic, self.start, self.end)
    __repr__ = __str__

    def to_json_dict(self):
        return {
            "algebraic": self.algebraic,
            "start":     self.start,
            "end":       self.end,
            "castle":    self.castle,
        }


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
    if end[1] == 6:
        if b.can_castle(color, kingside):
            for file in (4, 5, 6):
                if in_check(b, color, (rank, file)):
                    return False
            return (color, kingside)
    elif end[1] == 2:
        if b.can_castle(color, queenside):
            for file in (4, 3, 2):
                if in_check(b, color, (rank, file)):
                    return False
            return (color, queenside)
    return False


def in_check(b, color, position=None):
    """
    Returns true if the king would be in check if it were in the given position.
    If no position is given, the location of the king is pulled from the board.
    """
    board_positions = list(b.find(board.Piece(color, king)))
    if len(board_positions) != 1:
        raise Exception("Board has %d %s kings" % (
            len(board_positions), color))
    board_position = board_positions[0]
    if position is None:
        position = board_position
    else:
        b = copy.deepcopy(b)
        b[position] = b[board_position]
        b[board_position] = None
    for rank, file, piece in b:
        if piece.color == color:
            continue
        if _move_is_valid(b, (rank, file), position):
            return True
    return False


def in_checkmate(b, color):
    positions = list(b.find(board.Piece(color, king)))
    if len(positions) != 1:
        raise Exception("Board has %d %s kings" % (len(positions), color))
    position = positions[0]
    # See if the king can escape on his own
    for d_rank in (-1, 0, 1):
        for d_file in (-1, 0, 1):
            if not (0 <= position[0] + d_rank < 8):
                continue
            if not (0 <= position[1] + d_rank < 8):
                continue
            check_pos = (position[0] + d_rank, position[1] + d_file)
            # Check to make sure a friendly piece isn't blocking this position
            if (d_rank, d_file) != (0, 0):
                existing_piece = b[check_pos]
                if existing_piece is not None and existing_piece.color == color:
                    continue
            if not in_check(b, color, check_pos):
                return False
    threats = filter(lambda t: t[2].color != color,
                     pieces_with_access(b, position))
    # If there's more than one threat and we can't move out of check, poor old
    # king is hosed; you can't capture two pieces in a single move.
    if len(threats) > 1:
        return True
    # See if other pieces can capture the threatening piece
    tr, tf, threat = threats[0]
    for _, _, cap in pieces_with_access(b, (tr, tf)):
        # We already checked the king, don't take it into account here.
        if cap.piece == king:
            continue
        if cap.color == color:
            return False
    # See if pieces can move between the threatening piece and the king
    def is_blockable(rank, file):
        for _, _, blocker in pieces_with_access(b, (rank, file)):
            if blocker.color == color:
                return True
        return False
    if any(_check_between((tr, tf), position, is_blockable)):
        return False
    # If this threat can't be taken, and the king can't move out of the way,
    # checkmate, motherfucker.
    return True


def pieces_with_access(b, pos):
    """
    Returns the pieces on the board with access to the given position.
    """
    for rank, file, p in b:
        if _move_is_valid(b, (rank, file), pos):
            yield rank, file, p


def _check_between(start, end, func):
    """
    Evaluates func at every square between the start and end point,
    noninclusive. Can only move along ranks, files or diagonals. func should be
    a function that takes two parameters: rank and file. Yields the results of
    the evaluations in an unspecified order.
    """
    start_rank, start_file = start
    end_rank, end_file = end
    min_rank, max_rank = min(start_rank, end_rank), max(start_rank, end_rank)
    min_file, max_file = min(start_file, end_file), max(start_file, end_file)
    d_rank = max_rank - min_rank
    d_file = max_file - min_file
    if d_rank == 0:
        for f in range(min_file + 1, max_file):
            yield func(min_rank, f)
    elif d_file == 0:
        for r in range(min_rank + 1, max_rank):
            yield func(r, min_file)
    elif d_rank == d_file:
        d = max_file - min_file
        if max_file == end_file:
            sign_file = 1
        else:
            sign_file = -1
        if max_rank == end_rank:
            sign_rank = 1
        else:
            sign_rank = -1
        for i in range(1, d):
            yield func(start_rank + sign_rank * i, start_file + sign_file * i)
    else:
        raise ValueError(
            "Can't determine betweenness if d_rank and d_file aren't equal, or "
            "if one isn't zero. (d_rank=%s, d_file=%s)" % (d_rank, d_file))


def _any_between(b, start, end):
    """
    Returns true if there are any pieces between the start and end point,
    noninclusive. Can only move along ranks, files or diagonals.
    """
    return any(_check_between(
        start, end, lambda rank, file: b[rank, file] is not None))


def _pawn_move_is_valid(b, start, end):
    # Ugh.
    start_p = b[start]
    end_p = b[end]
    start_rank, start_file = start
    end_rank, end_file = end
    if end_p is None:
        # Check for en-passant if we're not moving to an occupied square and
        # we've moved out of our file.
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
        # Gotta be checking colors in here, so we can check if the pawn can move
        # forward 2 spots or just 1.
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
        # We're capturing.
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
    return abs(start_rank - end_rank) <= 1 and abs(start_file - end_file) <= 1

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

def _move_is_valid(b, start, end):
    if not 0 <= start[0] <= 7 or not 0 <= start[1] <= 7:
        return False
    if not 0 <= end[0] <= 7 or not 0 <= end[1] <= 7:
        return False
    start_p = b[start]
    if start_p is None:
        return False
    end_p = b[end]
    # Can't capture our own pieces, that would be dumb.
    if end_p is not None and start_p.color == end_p.color:
        return False
    if start_p.piece == pawn:
        if not _pawn_move_is_valid(b, start, end):
            return False
        return not _any_between(b, start, end)
    if start_p.piece == rook:
        if not _rook_move_is_valid(start, end):
            return False
        return not _any_between(b, start, end)
    if start_p.piece == king:
        if not _king_move_is_valid(b, start, end):
            return False
        return not _any_between(b, start, end)
    if start_p.piece == knight:
        # Knights get to hop over the other nerds, don't check for any_between.
        return _knight_move_is_valid(start, end)
    if start_p.piece == bishop:
        if not _bishop_move_is_valid(start, end):
            return False
        return not _any_between(b, start, end)
    if start_p.piece == queen:
        if not _queen_move_is_valid(start, end):
            return False
        return not _any_between(b, start, end)
    raise NotImplementedError("No rules for piece " + start_p.piece)
