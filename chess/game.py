import json

from chess import algebraic
from chess import board
from chess import move
from chess.const import *

class InvalidMoveError(Exception):
    pass

class Game(object):
    def __init__(self, boards, moves, to_play):
        self.boards = boards
        self.moves = moves
        self.to_play = to_play

    @classmethod
    def new(cls):
        return Game([board.Board.new()], [], white)

    @classmethod
    def from_json_dict(cls, jobj):
        boards = [board.Board.from_json_dict(b) for b in jobj["boards"]]
        moves = [move.Move.from_json_dict(m) for m in jobj["moves"]]
        to_play = jobj["to_play"]
        return cls(boards, moves, to_play)

    @property
    def current_board(self):
        return self.boards[-1]

    def algebraic_move(self, m):
        try:
            parsed = algebraic.parse_algebraic(
                self.current_board, self.to_play, m)
        except Exception as e:
            raise InvalidMoveError(e)
        self.move(parsed)

    def move(self, m):
        if not m.is_valid(self.current_board):
            raise InvalidMoveError("Move %s is invalid." % m)
        start_piece = self.current_board[m.start]
        if start_piece is None or start_piece.color != self.to_play:
            raise InvalidMoveError(
                "Piece at %s is %s, but it is %s's turn." %
                (move.location_str(m.start), start_piece,
                 color_names[self.to_play]))
        self.boards.append(self.current_board.apply(m))
        self.moves.append(m)
        if self.to_play == white:
            self.to_play = black
        else:
            self.to_play = white

    def summary(self, sep=" "):
        pairs = [self.moves[i:i+2] for i in range(0, len(self.moves), 2)]
        pair_strs = []
        for i, pair in enumerate(pairs):
            if len(pair) == 1:
                pair_strs.append("%d.%s" % (i + 1, pair[0].algebraic))
            else:
                pair_strs.append("%d.%s %s" % (
                    i + 1, pair[0].algebraic, pair[1].algebraic))
        return sep.join(pair_strs)

    def __str__(self):
        return "Game with %d moves, %s to play" % (
            len(self.moves), color_names[self.to_play])

    def to_json_dict(self):
        return {
            "boards":  [b.to_json_dict() for b in self.boards],
            "moves":   [m.to_json_dict() for m in self.moves],
            "to_play": self.to_play,
        }
