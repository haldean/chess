import chess
import emails
import engine.store
import flask
import json
import os
import validate_email

from flask.ext import socketio

use_debug = False
app = flask.Flask("chess")
rstore = engine.store.RedisStore()
sockapp = socketio.SocketIO(app)

@app.route("/")
def index():
    return flask.render_template("index.html")

def _to_game_url(link):
    return "%sgame/%s" % (flask.request.url_root, link)

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
    white_link, black_link = rstore.start_game(white_email, black_email)
    white_url = _to_game_url(white_link)
    black_url = _to_game_url(black_link)
    emails.send_welcome(white_email, white_url, black_email)
    emails.send_welcome(black_email, black_url, white_email)
    return flask.redirect(flask.url_for("getready"))

@app.route("/getready")
def getready():
    return flask.render_template("post_start.html")

def _make_move(game_link):
    color, game_id, game = rstore.game_from_link(game_link)
    if color != game.to_play:
        flask.abort(403)
    move_str = flask.request.form["move"]
    move = chess.parse_algebraic(
        game.current_board, color, move_str)
    rstore.move(game_id, move)
    if color == chess.white:
        opponent = chess.black
    else:
        opponent = chess.white
    player_email, _ = rstore.get_user(game_id, color)
    opponent_email, opponent_link = rstore.get_user(game_id, opponent)
    emails.send_move_email(
        opponent_email, _to_game_url(opponent_link), player_email, move_str)
    # Reload all the other players.
    sockapp.emit("reload", "", room=game_id)

@app.route("/game/<game_link>", methods=["GET", "POST"])
def game(game_link):
    if flask.request.method == "POST":
        _make_move(game_link)
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

def run(api_keys):
    app.secret_key = api_keys.flask_session_key
    emails.set_mailgun_key(api_keys.mailgun_key)
    # Jinja does some funny shit here; just set the app directory to the
    # directory that web.py is in.
    app.root_path = os.path.abspath(os.path.dirname(__file__))
    if use_debug:
        app.run(debug=True)
    else:
        sockapp.run(app)
