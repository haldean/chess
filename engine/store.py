import base64
import chess
import json
import os
import redis
import uuid

_REDIS_PORT = 6379
_REDIS_PREFIX = ""

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

class RedisStore(object):
    def __init__(self):
        self.rconn = redis.StrictRedis(host="localhost", port=_REDIS_PORT, db=0)
        self.rconn.setnx(_REDIS_PREFIX + "chess:games:nextid", 0)

    def begin(self):
        id = self.rconn.incr(_REDIS_PREFIX + "chess:games:nextid")
        game = chess.Game.new()
        self._set_game(id, game)
        return id, game

    def get(self, id):
        game_str = self.rconn.get(_REDIS_PREFIX + "chess:games:%s:game" % id)
        return chess.Game.from_json_dict(json.loads(game_str))

    def all_games(self):
        # Warning: expensive!
        keys = self.rconn.keys(_REDIS_PREFIX + "chess:games:*:game")
        game_ids = sorted([k.split(':')[-2] for k in keys])
        games = []
        for game_id in game_ids:
            game = self.get(game_id)
            white_email, white_link = self.get_user(game_id, chess.white)
            black_email, black_link = self.get_user(game_id, chess.black)
            games.append(dict(
                game_id=game_id, game=game,
                white_email=white_email, white_link=white_link,
                black_email=black_email, black_link=black_link,
            ))
        return games

    def game_from_link(self, link):
        color, game_id = json.loads(self.rconn.get(
            _REDIS_PREFIX + "chess:links:%s" % link))
        return color, game_id, self.get(game_id)

    def _pick_link(self):
        link = None
        while True:
            link = base64.b32encode(os.urandom(5)).lower()
            if not self.rconn.exists(_REDIS_PREFIX + "chess:links:%s" % link):
                return link

    def start_game(self, white_email, black_email):
        game_id, _ = self.begin()
        white_link = self._pick_link()
        black_link = self._pick_link()
        # Create link-to-game mapping
        self.rconn.set(
            _REDIS_PREFIX + "chess:links:%s" % white_link,
            json.dumps((chess.white, game_id)))
        self.rconn.set(
            _REDIS_PREFIX + "chess:links:%s" % black_link,
            json.dumps((chess.black, game_id)))
        # Create game-to-email mapping
        self.rconn.set(
            _REDIS_PREFIX + "chess:games:%s:%s:email" % (game_id, chess.white),
            white_email)
        self.rconn.set(
            _REDIS_PREFIX + "chess:games:%s:%s:email" % (game_id, chess.black),
            black_email)
        # Create game-to-link mapping
        self.rconn.set(
            _REDIS_PREFIX + "chess:games:%s:%s:link" % (game_id, chess.white),
            white_link)
        self.rconn.set(
            _REDIS_PREFIX + "chess:games:%s:%s:link" % (game_id, chess.black),
            black_link)
        return white_link, black_link

    def get_user(self, game_id, color):
        email_addr = self.rconn.get(
            _REDIS_PREFIX + "chess:games:%s:%s:email" % (game_id, color))
        link = self.rconn.get(
            _REDIS_PREFIX + "chess:games:%s:%s:link" % (game_id, color))
        return email_addr, link

    def move(self, id, move):
        game = self.get(id)
        game.move(move)
        self._set_game(id, game)

    def _set_game(self, game_id, game):
        self.rconn.set(
            _REDIS_PREFIX + "chess:games:%s:game" % game_id,
            json.dumps(game.to_json_dict()))
