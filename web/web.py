import flask
import os

app = flask.Flask("chess")

@app.route("/")
def index():
    return flask.render_template("index.html")

if __name__ == "__main__":
    # Jinja does some funny shit here; just set the app directory to the
    # directory that web.py is in.
    app.root_path = os.path.abspath(os.path.dirname(__file__))
    app.run(debug=True)
