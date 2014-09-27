white = 'w'
black = 'b'
colors = set((white, black))

pawn = 'p'
rook = 'R'
bishop = 'B'
knight = 'N'
queen = 'Q'
king = 'K'
pieces = set((pawn, rook, bishop, knight, queen, king))

kingside = 'ks'
queenside = 'qs'
all_castles = set((
    (white, kingside), (white, queenside),
    (black, kingside), (black, queenside),
))

ranks = set(str(x) for x in range(1, 9))
files = set(('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'))

color_names = {
    black: "black",
    white: "white",
}

piece_names = {
    pawn: "pawn",
    rook: "rook",
    knight: "knight",
    bishop: "bishop",
    queen: "queen",
    king: "king",
}
