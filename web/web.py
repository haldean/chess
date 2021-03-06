import argparse
import chess
import emails
import engine.store
import flask
import logs
import os
import stats
import utils
import validate_email

from flask.ext import socketio
from render_game import render_game
from render_user import render_user, render_user_dashboard

use_debug_server = False

app = flask.Flask("chess")
sockapp = socketio.SocketIO(app)

def debug_route(func):
    def _wrapped(*args, **kwargs):
        if flask.request.host.split(':')[0] == "localhost":
            return func(*args, **kwargs)
        flask.abort(404)
    _wrapped.__name__ = func.__name__
    return _wrapped

@app.route("/")
@logs.wrap
def index():
    return flask.render_template("index.html")

@app.route("/debug")
@logs.wrap
@debug_route
def debug():
    player_dashes = {}
    for player in rstore.all_players():
        if player:
            player_dashes[player] = rstore.get_player_dashboard(player)
    return flask.render_template(
        "debug.html", games=rstore.all_games(), players=player_dashes)

@app.route("/debug/create_game")
@logs.wrap
@debug_route
def debug_create_game():
    white_link, black_link, public_link, _ = rstore.start_game("", "")
    white_url = utils.to_game_url(white_link)
    black_url = utils.to_game_url(black_link)
    public_url = utils.to_game_url(public_link)
    return flask.render_template(
        "debug_create_game.html",
        white=white_url, black=black_url, public=public_url)

@app.route("/stats")
@logs.wrap
def global_stats():
    victories = stats.VictoryStats(rstore)
    plays = stats.PlayStats(rstore)
    return flask.render_template(
        "stats.html", victories=victories, plays=plays)

@app.route("/start", methods=["POST"])
@logs.wrap
def start():
    white_email = flask.request.form["white_email"]
    white_is_valid = validate_email.validate_email(white_email)
    black_email = flask.request.form["black_email"]
    black_is_valid = validate_email.validate_email(black_email)
    if not white_is_valid or not black_is_valid:
        print "Bad email addresses; %s (%s) %s (%s)" % (
            white_email, white_is_valid, black_email, black_is_valid)
        flask.abort(400)
    white_link, black_link, _, _ = rstore.start_game(white_email, black_email)
    white_url = utils.to_game_url(white_link)
    black_url = utils.to_game_url(black_link)
    emails.send_welcome(white_email, white_url, black_email)
    emails.send_welcome(black_email, black_url, white_email)
    return flask.redirect(flask.url_for("getready"))

@app.route("/getready")
@logs.wrap
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
    # Email addresses aren't set on debug games; don't try to send an email to
    # an empty address.
    if player_email and opponent_email:
        emails.send_move_email(
            opponent_email, utils.to_game_url(opponent_link),
            player_email, move_str)
    # Reload all the other players.
    sockapp.emit("reload", "", room=game_id)

@app.route("/game/<game_link>", methods=["GET", "POST"])
@logs.wrap
def game(game_link):
    if flask.request.method == "POST":
        _make_move(game_link)
        return "ok"
    color, game_id, game = rstore.game_from_link(game_link)
    if color is not None:
        opponent, _ = rstore.get_user(game_id, chess.opposite_color(color))
    else:
        opponent = None
    return render_game(color, game_id, game, opponent)

@app.route("/user")
@logs.wrap
def user_search():
    return flask.render_template("user_lookup.html")

@app.route("/user/<email_addr>")
@logs.wrap
def user(email_addr):
    return render_user(rstore, email_addr)

@app.route("/me/<dash_link>")
@logs.wrap
def dashboard(dash_link):
    return render_user_dashboard(rstore, dash_link)

@app.route("/manual-entry", methods=["GET", "POST"])
@logs.wrap
def manual_entry():
    if flask.request.method == "POST":
        white_email = flask.request.form["white_email"]
        black_email = flask.request.form["black_email"]
        white_link, black_link, public_link, game_id = rstore.start_game(
            white_email, black_email)
        pgn = flask.request.form["game"]
        game = chess.parse_pgn(pgn)
        rstore.set_game(game_id, game)
        if game.termination is None:
            white_url = utils.to_game_url(white_link)
            black_url = utils.to_game_url(black_link)
            emails.send_welcome(white_email, white_url, black_email)
            emails.send_welcome(black_email, black_url, white_email)
        return flask.redirect(utils.to_game_url(public_link))
    return flask.render_template("manual_entry.html")

@sockapp.on("join")
def on_join(data):
    # When clients join, we hook them into a room just for their game so that we
    # can force-reload them when the other player moves.
    link = data["link"]
    _, game_id, _ = rstore.game_from_link(link)
    socketio.join_room(game_id)

def run(api_keys):
    argspec = argparse.ArgumentParser(description="Runs the chess frontend")
    argspec.add_argument("--debug", help="use debug server", action="store_true")
    argspec.add_argument("--redis_host", default="localhost")
    args = argspec.parse_args()

    global rstore
    rstore = engine.store.RedisStore(host=args.redis_host)
    app.secret_key = api_keys.flask_session_key
    emails.set_mailgun_key(api_keys.mailgun_key)
    # Jinja does some funny shit here; just set the app directory to the
    # directory that web.py is in.
    app.root_path = os.path.abspath(os.path.dirname(__file__))
    if args.debug:
        app.run(host="0.0.0.0", debug=True)
    else:
        sockapp.run(app, host="0.0.0.0", log_file=logs.log_file)
