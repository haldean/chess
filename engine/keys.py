PUBLIC_LINK = "public"

def key_next_id():
    "Integer that represents the game ID for the next game to be played."
    return "chess:games:nextid"

def key_all_ids():
    "Set that contains the IDs of all games."
    return "chess:game_ids"

def key_game(game_id):
    "JSON-encoded game objects by game ID."
    return "chess:games:%s:game" % game_id

def key_game_from_link(link):
    "Pair of (color, game_id) for a given link string."
    return "chess:links:%s" % link

def key_players():
    "Set that contains the email addresses of all players."
    return "chess:players"

def key_email_from_game(game_id, color):
    "Maps a game ID and the color of the player to the player's email address."
    return "chess:games:%s:%s:email" % (game_id, color)

def key_link_from_game(game_id, color):
    "Maps a game ID and the color of the player to the player's link."
    return "chess:games:%s:%s:link" % (game_id, color)

def key_terminations(termination):
    "Set that contains the IDs of all games with a given termination."
    return "chess:terminations:%s" % termination

def key_game_lengths():
    "Mapping of game length (in plys) to frequency."
    return "chess:stats:game_lengths"

def key_player_games(email):
    "Set of game IDs played by a given player."
    return "chess:player_games:%s" % email
