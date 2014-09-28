import chess

class InMemoryStore(object):
    def __init__(self):
        self._games = {}
        self._next_id = 0

    def begin(self):
        id = self._next_id
        self._next_id += 1
        self._games[id] = chess.Game.new()
        return id, self._games[id]

    def get(self, id):
        return self._games.get(id, None)

    def move(self, id, move):
        self._games[id].move(move)
