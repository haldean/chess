import store

rstore = store.RedisStore()

def populate_terminations():
    for game in rstore.all_games():
        rstore.set_game(game["game_id"], game["game"])

def populate_game_ids():
    keys = rstore.rconn.keys("chess:games:*:game")
    game_ids = [k.split(":")[-2] for k in keys]
    rstore.rconn.sadd("chess:game_ids", *game_ids)

def populate_players():
    keys = rstore.rconn.keys("chess:games:*:*:email")
    players = set()
    for k in keys:
        val = rstore.rconn.get(k)
        if val:
            players.add(k)
    rstore.rconn.sadd("chess:players", *players)
