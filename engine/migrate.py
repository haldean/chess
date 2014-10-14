import store

rstore = store.RedisStore()

def populate_terminations():
    for game in rstore.all_games():
        rstore.set_game(game["game_id"], game["game"])
