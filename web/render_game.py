import chess
import eco
import flask
import json
import stats

eco_data = eco.load_default()

def termination_str(game, color):
    if color is None:
        if game.termination == chess.white_victory:
            return "Game over &mdash; white wins"
        elif game.termination == chess.black_victory:
            return "Game over &mdash; black wins"
        return "Stalemate."
    if color == chess.white and game.termination == chess.white_victory:
        if chess.in_checkmate(game.current_board, chess.black):
            return "Checkmate &mdash; you win!"
        return "Game over &mdash; you win!"
    elif color == chess.black and game.termination == chess.black_victory:
        if chess.in_checkmate(game.current_board, chess.white):
            return "Checkmate &mdash; you win!"
        return "Game over &mdash; you win!"
    elif game.termination == chess.stalemate:
        return "Stalemate."
    else:
        if chess.in_checkmate(game.current_board, color):
            return "Checkmate &mdash; you lose."
        return "Game over &mdash; you lose."

def linkify_summary(game):
    def linkify_move(i, m):
        return "<a class=\"move_link\" id=\"move%d\" href=\"#board-%d\">%s</a>" % (
            i + 1, i + 1, m.algebraic)
    move_links = map(lambda x: linkify_move(*x), enumerate(game.moves))
    pairs = [move_links[i:i+2] for i in range(0, len(move_links), 2)]
    res = []
    for i, pair in enumerate(pairs):
        if len(pair) == 1:
            res.append("%d.%s" % (i + 1, pair[0]))
        else:
            res.append("%d.%s %s" % (i + 1, pair[0], pair[1]))
    if game.termination:
        res.append(game.termination)
    return "<br>".join(res)

def render_game(color, game_id, game, opponent):
    access = chess.accessibility_map(game.current_board);
    if game.to_play is None:
        to_play = "nobody"
    else:
        to_play = chess.color_names[game.to_play]
    if game.termination is None:
        termination = "undefined"
        termination_msg = None
    else:
        termination = "'%s'" % game.termination
        termination_msg = termination_str(game, color)
    if color is None:
        color_name = None
    else:
        color_name = chess.color_names[color]
    stat_obj = stats.Stats(game, eco_data)
    return flask.render_template(
        "game.html",
        game=json.dumps(game.to_json_dict()),
        to_play=to_play,
        termination=termination,
        termination_msg=termination_msg,
        color_name=color_name,
        player=color,
        summary=linkify_summary(game),
        accessibility=json.dumps(access),
        opponent=opponent,
        stats=stat_obj,
        )
