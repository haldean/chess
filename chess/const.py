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
