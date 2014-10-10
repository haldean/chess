import flask
import os

app = flask.Flask("chess")
sqlc = psychopg2.connect("dbname='chess' host='localhost'")

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/game")
def game():
    return flask.render_template("game.html")

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
