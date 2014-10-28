import argparse
import store

from keys import *

class Migrator(object):
    def __init__(self, rstore):
        self.rstore = rstore

    def populate_terminations(self):
        for game in self.rstore.all_games():
            self.rstore.set_game(game["game_id"], game["game"])

    def populate_game_ids(self):
        keys = self.rstore.rconn.keys(key_game("*"))
        game_ids = [k.split(":")[-2] for k in keys]
        for game_id in game_ids:
            self.rstore.rconn.sadd(key_all_ids(), game_id)

    def populate_players(self):
        keys = self.rstore.rconn.keys(key_email_from_game("*", "*"))
        players = set()
        for k in keys:
            val = self.rstore.rconn.get(k)
            if val:
                players.add(val)
                self.rstore.rconn.sadd(key_players(), val)

    def populate_player_games(self):
        keys = self.rstore.rconn.keys(key_email_from_game("*", "*"))
        for k in keys:
            game_id = k.split(":")[2]
            email = self.rstore.rconn.get(k)
            if email:
                self.rstore.rconn.sadd(key_player_games(email), game_id)

CURRENT_MIGRATIONS = [
    Migrator.populate_player_games,
    ]

if __name__ == "__main__":
    argspec = argparse.ArgumentParser(description="Migrates data in redis")
    argspec.add_argument("--redis_host", default="localhost")
    args = argspec.parse_args()
    rstore = store.RedisStore(host=args.redis_host)
    migrator = Migrator(rstore)
    for migration in CURRENT_MIGRATIONS:
        migration(migrator)
