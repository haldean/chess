import flask

def to_game_url(link):
    return "%sgame/%s" % (flask.request.url_root, link)
