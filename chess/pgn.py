import re

from chess import algebraic
from chess import game
from chess.const import *

pgn_metadata_re = re.compile('\s*\[.*\]\s*')
move_no_re = re.compile('^\d+\.')

def parse_pgn(pgn):
    g = game.Game.new()
    pgn = pgn.split("\n")
    for i, line in enumerate(pgn):
        if pgn_metadata_re.match(line):
            continue
        if not line:
            continue
        pgn = pgn[i:]
        break
    pgn = filter(lambda x: x, pgn)
    ply_no = 1
    for line in pgn:
        split = line.strip().split(" ")
        for i, m_str in enumerate(split):
            if move_no_re.match(m_str):
                m_str = m_str[m_str.find(".")+1:]
            if m_str in ("0-1", "1-0", "1/2-1/2"):
                g.termination = m_str
                break
            try:
                m = algebraic.parse_algebraic(g.current_board, g.to_play, m_str)
                g.move(m)
            except Exception as e:
                raise ValueError(
                        "Failed to parse move %d (%s) for %s (%s) on\n%s" % (
                    ply_no, m_str, color_names[g.to_play], e, g.current_board))
            ply_no += 1
    return g

def read_pgn(fname):
    with open(fname, 'r') as f:
        return parse_pgn(f.read())
