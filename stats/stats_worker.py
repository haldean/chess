import argparse
import stats_store
from engine import store

def aggregate(rstore):
    games = rstore.all_games()
    game_lengths = {}
    max_len = max(len(g["game"].moves) for g in games)
    for i in range(max_len + 1):
        game_lengths[i] = 0
    for g in games:
        game = g["game"]
        game_lengths[len(game.moves)] += 1
    for game_len, freq in game_lengths.iteritems():
        rstore.rconn.hset("chess:stats:game_lengths", game_len, freq)

if __name__ == "__main__":
    argspec = argparse.ArgumentParser(description="Updates cached statistics")
    argspec.add_argument("--redis_host", default="localhost")
    args = argspec.parse_args()
    rstore = stats_store.wrap(store.RedisStore(host=args.redis_host))
    aggregate(rstore)
