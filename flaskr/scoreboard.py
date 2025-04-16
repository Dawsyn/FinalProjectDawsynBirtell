from flask import Blueprint, render_template
import sqlite3

bp = Blueprint('scoreboard', __name__, url_prefix='/scoreboard')

@bp.route('/')
def index():
    print("🎯 scoreboard route hit")
    conn = sqlite3.connect("instance/flaskr.sqlite")
    conn.row_factory = sqlite3.Row
    scores = conn.execute("SELECT * FROM scoreboard ORDER BY game_date DESC").fetchall()
    conn.close()
    return render_template('scoreboard/scoreboard.html', scores=scores)
