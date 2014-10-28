import base64
import chess
import json
import os
import redis
import uuid

from engine.keys import *

class RedisStore(object):
    def __init__(self, host, port=6379, db=0):
        self.rconn = redis.StrictRedis(host=host, port=port, db=db)
        self.rconn.setnx(key_next_id(), 0)

    def begin(self):
        id = self.rconn.incr(key_next_id())
        self.rconn.sadd(key_all_ids(), id)
        game = chess.Game.new()
        self.set_game(id, game)
        return id, game

    def get(self, id):
        game_str = self.rconn.get(key_game(id))
        return chess.Game.from_json_dict(json.loads(game_str))

    def all_games(self):
        game_ids = sorted(self.rconn.smembers(key_all_ids()))
        games = []
        for game_id in game_ids:
            game = self.get(game_id)
            white_email, white_link = self.get_user(game_id, chess.white)
            black_email, black_link = self.get_user(game_id, chess.black)
            public_link = self.get_public_link(game_id)
            games.append(dict(
                game_id=game_id, game=game,
                white_email=white_email, white_link=white_link,
                black_email=black_email, black_link=black_link,
                public_link=public_link,
            ))
        return games

    def game_from_link(self, link):
        color, game_id = json.loads(self.rconn.get(key_game_from_link(link)))
        if color == PUBLIC_LINK:
            color = None
        return color, game_id, self.get(game_id)

    def _pick_link(self):
        link = None
        while True:
            link = base64.b32encode(os.urandom(5)).lower()
            if not self.rconn.exists(key_game_from_link(link)):
                return link

    def start_game(self, white_email, black_email):
        game_id, _ = self.begin()
        white_link = self._pick_link()
        black_link = self._pick_link()
        public_link = self._pick_link()
        self.rconn.sadd(key_players(), white_email)
        self.rconn.sadd(key_players(), black_email)
        # Create link-to-game mapping
        self.rconn.set(
            key_game_from_link(white_link), json.dumps((chess.white, game_id)))
        self.rconn.set(
            key_game_from_link(black_link), json.dumps((chess.black, game_id)))
        self.rconn.set(
            key_game_from_link(public_link), json.dumps((PUBLIC_LINK, game_id)))
        # Create game-to-email mapping
        self.rconn.set(key_email_from_game(game_id, chess.white), white_email)
        self.rconn.set(key_email_from_game(game_id, chess.black), black_email)
        # Create game-to-link mapping
        self.rconn.set(key_link_from_game(game_id, chess.white), white_link)
        self.rconn.set(key_link_from_game(game_id, chess.black), black_link)
        self.rconn.set(key_link_from_game(game_id, PUBLIC_LINK), public_link)
        # Create email-to-game mapping
        self.rconn.sadd(key_player_games(white_email), game_id)
        self.rconn.sadd(key_player_games(black_email), game_id)
        return white_link, black_link, public_link, game_id

    def user_exists(self, email_addr):
        return self.rconn.exists(key_player_games(email_addr))

    def get_user(self, game_id, color):
        email_addr = self.rconn.get(key_email_from_game(game_id, color))
        link = self.rconn.get(key_link_from_game(game_id, color))
        return email_addr, link

    def get_public_link(self, game_id):
        return self.rconn.get(key_link_from_game(game_id, PUBLIC_LINK))

    def move(self, id, move):
        game = self.get(id)
        game.move(move)
        self.set_game(id, game)

    def set_game(self, game_id, game):
        self.rconn.set(key_game(game_id), json.dumps(game.to_json_dict()))
        if game.termination:
            self.rconn.sadd(key_terminations(game.termination), game_id)
