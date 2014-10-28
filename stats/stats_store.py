import chess

from engine import keys
from engine import store

class StatsStore(store.RedisStore):
    def __init__(self, rstore):
        self.rconn = rstore.rconn

    def terminations(self):
        res = {}
        for t in (chess.white_victory, chess.black_victory, chess.stalemate):
            res[t] = self.rconn.scard(keys.key_terminations(t))
        return res

    def game_count(self):
        return self.rconn.scard(keys.key_all_ids())

    def player_count(self):
        return self.rconn.scard(keys.key_players())

    def game_lengths(self):
        return self.rconn.hgetall(keys.key_game_lengths())

    def games_for_player(self, player):
        return self.rconn.smembers(keys.key_player_games(player))

def wrap(rstore):
    return StatsStore(rstore)
