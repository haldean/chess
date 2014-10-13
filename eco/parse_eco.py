import cPickle as pickle
import chess
import datetime
import re
import tree

from os import path

def eco_to_move(board, eco_move):
    loc1 = eco_move[:2]
    loc2 = eco_move[2:]
    start = chess.loc_from_str(loc1)
    end = chess.loc_from_str(loc2)
    return chess.Move.on_board(start, end, board)

def find_summary(opening_moves):
    moves = []
    board = chess.Board.new()
    for eco_move in opening_moves:
        move = eco_to_move(board, eco_move)
        board = board.apply(move)
        moves.append(move)
    pairs = [(moves[i], moves[i+1]) for i in range(0, len(moves) - 1, 2)]
    if len(moves) % 2 != 0:
        pairs.append((moves[-1], None))
    def to_str(i, pair):
        if pair[1]:
            return "%d.%s %s" % (i, pair[0].algebraic, pair[1].algebraic)
        else:
            return "%d.%s" % (i, pair[0].algebraic)
    return " ".join(to_str(i, p) for i, p in enumerate(pairs))

def parse(fname):
    data = []
    with open(fname, 'r') as f:
        for line in f:
            data.append(line)
    data = map(lambda x: x.strip(), data)
    data = filter(lambda x: not x.startswith('-'), data)
    opening_pairs = []
    current_opening = []
    for line in data:
        if re.match('^[A-E][\d]+', line):
            if current_opening:
                opening_pairs.append(current_opening)
            current_opening = [line]
        elif line.startswith("("):
            current_opening[-1] += " " + line
        elif len(current_opening) == 1:
            current_opening.append(line)
        elif current_opening:
            current_opening[-1] += " " + line
    opening_pairs.append(current_opening)
    openings = []
    for opening in opening_pairs:
        assert opening[1].startswith("1.")
        code, name = opening[0].split(" ", 1)
        moves = opening[1][2:].split()
        openings.append(tree.Opening(code, name, moves, find_summary(moves)))
    return openings

def make_tree(openings):
    root = tree.EcoNode()
    for opening in openings:
        root.insert(opening)
    return root

def load_default():
    pickle_file = path.join(path.dirname(__file__), "eco.pickle")
    if path.exists(pickle_file):
        with open(pickle_file, 'r') as f:
            return pickle.load(f)
    print "Loading ECO data, this may take some time..."
    start = datetime.datetime.now()
    openings = parse(path.join(path.dirname(__file__), "eco.raw"))
    tree = make_tree(openings)
    time = datetime.datetime.now() - start
    print "Loaded %s openings in %s" % (len(openings), time)
    print "Caching in %s" % pickle_file
    with open(pickle_file, 'w') as f:
        pickle.dump(tree, f)
    return tree

if __name__ == '__main__':
    import pprint
    tree = load_default()
    pprint.pprint(tree.all_submoves())
