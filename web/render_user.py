import chess
import eco
import flask
import stats
import utils

eco_data = eco.load_default()

def render_recent_game(game_stats, use_public_link=True):
    if use_public_link:
        link = game_stats.public_link
    else:
        link = game_stats.player_link
    game_str = "Game against %s" % game_stats.opponent
    return "<a href='%s'>%s</a>" % (utils.to_game_url(link), game_str)

def render_user(rstore, email_addr):
    if not rstore.user_exists(email_addr):
        return flask.render_template("user_404.html", email=email_addr)
    player_stats = stats.PlayerStats(rstore, email_addr, eco_data)
    rendered_games = {}
    for k, v in player_stats.game_stats.iteritems():
        rendered_games[k] = render_recent_game(v)
    return flask.render_template(
        "user.html",
        player=player_stats,
        game_stats=rendered_games,
        )

def render_user_dashboard(rstore, dash_link):
    email = rstore.get_player_from_dashboard(dash_link)
    player_stats = stats.PlayerStats(rstore, email, eco_data)
    rendered_games = []
    for game_id in player_stats.in_progress:
        rendered_games.append(render_recent_game(
            player_stats.game_stats[game_id], use_public_link=False))
    return flask.render_template(
        "dashboard.html",
        email=email,
        in_progress=rendered_games,
        )
