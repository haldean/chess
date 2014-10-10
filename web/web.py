import chess
import engine.store
import flask
import json
import os
import validate_email

from flask.ext import socketio

app = flask.Flask("chess")
rstore = engine.store.RedisStore()
sockapp = socketio.SocketIO(app)

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    white_email = flask.request.form["white_email"]
    white_is_valid = validate_email.validate_email(white_email)
    black_email = flask.request.form["black_email"]
    black_is_valid = validate_email.validate_email(black_email)
    if not white_is_valid or not black_is_valid:
        print "Bad email addresses; %s (%s) %s (%s)" % (
            white_email, white_is_valid, black_email, black_is_valid)
        flask.abort(400)
    game_id, _ = rstore.begin()
    white_link, black_link = rstore.create_link(game_id)
    print white_link, black_link

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
        # Reload all the other players.
        sockapp.emit("reload", "", room=game_id)
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

@sockapp.on("join")
def on_join(data):
    # When clients join, we hook them into a room just for their game so that we
    # can force-reload them when the other player moves.
    link = data["link"]
    _, game_id, _ = rstore.game_from_link(link)
    socketio.join_room(game_id)

if __name__ == "__main__":
    # Jinja does some funny shit here; just set the app directory to the
    # directory that web.py is in.
    app.root_path = os.path.abspath(os.path.dirname(__file__))
    sockapp.run(app)
    #app.run(debug=True)
