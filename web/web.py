import chess
import engine.store
import flask
import json
import os

app = flask.Flask("chess")
rstore = engine.store.RedisStore()

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/game/<game_link>")
def game(game_link):
    color, game_id, game = rstore.game_from_link(game_link)
    access = chess.accessibility_map(game.current_board);
    return flask.render_template(
        "game.html",
        game=json.dumps(game.to_json_dict()),
        player=color,
        summary=game.summary(),
        accessibility=json.dumps(access))

@app.route("/login")
def login():
    return flask.render_template("login.html")

@app.route("/do_login", methods=["POST"])
def do_login():
    user = flask.request.form["user"]
    password = flask.request.form["pass"]

if __name__ == "__main__":
    # Jinja does some funny shit here; just set the app directory to the
    # directory that web.py is in.
    app.root_path = os.path.abspath(os.path.dirname(__file__))
    app.run(debug=True)
