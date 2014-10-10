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

@app.route("/game/<game_link>", methods=["GET", "POST"])
def game(game_link):
    if flask.request.method == "POST":
        color, game_id, game = rstore.game_from_link(game_link)
        if color != game.to_play:
            flask.abort(403)
        move_str = flask.request.form["move"]
        move = chess.parse_algebraic(
            game.current_board, color, move_str)
        rstore.move(game_id, move)
        return "ok"
    color, game_id, game = rstore.game_from_link(game_link)
    access = chess.accessibility_map(game.current_board);
    return flask.render_template(
        "game.html",
        game=json.dumps(game.to_json_dict()),
        to_play=chess.color_names[game.to_play],
        color_name=chess.color_names[color],
        player=color,
        summary=game.summary("\n"),
        accessibility=json.dumps(access))

if __name__ == "__main__":
    # Jinja does some funny shit here; just set the app directory to the
    # directory that web.py is in.
    app.root_path = os.path.abspath(os.path.dirname(__file__))
    app.run(debug=True)
