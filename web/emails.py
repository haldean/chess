import flask
import requests

mailgun_key = None

def set_mailgun_key(mgkey):
    global mailgun_key
    mailgun_key = mgkey

def send_welcome(addr, link, other_email):
    return requests.post(
        "https://api.mailgun.net/v2/tokd.wtf/messages",
        auth=("api", mailgun_key),
        data={
            "from": "Chessmaster <chess@tokd.wtf>",
            "to": [addr],
            "subject": "Your chess game with %s has begun" % other_email,
            "text": "Come play chess! Your unique game link (don't share it "
                    "with others) is %s" % link,
            "html": flask.render_template(
                "welcome_email.html", game_url=link, other_email=other_email),
        })

def send_move_email(addr, link, other_email, last_move):
    return requests.post(
        "https://api.mailgun.net/v2/tokd.wtf/messages",
        auth=("api", mailgun_key),
        data={
            "from": "Chessmaster <chess@tokd.wtf>",
            "to": [addr],
            "subject": "Your move against %s" % other_email,
            "text": "It's your turn! Your unique game link (in case you "
                    "forgot it) is %s" % link,
            "html": flask.render_template(
                "move_email.html",
                game_url=link, other_email=other_email, last_move=last_move),
        })
