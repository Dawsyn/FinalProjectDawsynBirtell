from flask import Blueprint, render_template, request
from flask import redirect, url_for
from datetime import datetime
import sqlite3

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@api_bp.route('/scoreboard')
def show_scores():
    conn = sqlite3.connect("instance/flaskr.sqlite")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get all distinct game dates from DB
    cur.execute("SELECT DISTINCT game_date FROM scoreboard ORDER BY game_date DESC")
    all_dates = [row["game_date"] for row in cur.fetchall()]

    # Format today’s date to match game_date format
    today = datetime.today().strftime("%m/%d/%Y")

    # Determine selected date: GET param -> today if in list -> most recent date
    selected_date = request.args.get("date")
    if not selected_date:
        if today in all_dates:
            selected_date = today
        elif all_dates:
            selected_date = all_dates[0]
        else:
            selected_date = None

    # Fetch scores for the selected date if there is one
    scores = []
    if selected_date:
        cur.execute("SELECT * FROM scoreboard WHERE game_date = ?", (selected_date,))
        scores = cur.fetchall()

    conn.close()
    return "<h1>Hello from the route!</h1>"

    #return render_template("scores.html", scores=scores, all_dates=all_dates, selected_date=selected_date)
