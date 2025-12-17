from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/<user>")
def show(user=None):
    """Show shutdown info for a given user."""
    return render_template("index.html", user=user or "home")


if __name__ == "__main__":
    app.run(host="localhost", port=6789, debug=True)
