import functools

@functools.total_ordering
class Opening(object):
    def __init__(self, code, name, moves):
        self.code = code
        self.name = name
        self.moves = moves

    def __lt__(self, other):
        return len(self.moves) < len(other.moves)

    def __eq__(self, other):
        return len(self.moves) == len(other.moves)

    def __str__(self):
        return "[%s] %s (%d plies)" % (self.code, self.name, len(self.moves))
    __repr__ = __str__

class EcoNode(object):
    def __init__(self, moves=None, children=None):
        if moves is None:
            moves = []
        self.moves = moves
        if children is None:
            children = {}
        self.children = children

    def insert(self, opening, moves_remaining=None):
        if moves_remaining is None:
            moves_remaining = opening.moves
        if not moves_remaining:
            self.moves.append(opening)
        else:
            next_move = moves_remaining[0]
            if next_move not in self.children:
                self.children[next_move] = EcoNode()
            self.children[next_move].insert(opening, moves_remaining[1:])

    def all_submoves(self):
        moves = list(self.moves)
        for child in self.children.itervalues():
            moves.extend(child.all_submoves())
        return moves

