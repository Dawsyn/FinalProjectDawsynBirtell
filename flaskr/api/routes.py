from flask import Blueprint, jsonify, render_template
import sqlite3

api_bp = Blueprint('api', __name__)

""" @api_bp.route('/scoreboard')
def get_scoreboard():
    return jsonify({"message": "API is working!"}) """

@api_bp.route('/scoreboard')
def show_scores():
    conn = sqlite3.connect("instance/flaskr.sqlite")
    conn.row_factory = sqlite3.Row
    scores = conn.execute("SELECT * FROM scores ORDER BY game_date DESC").fetchall()
    conn.close()
    return render_template("scoreboard/scoreboard.html", scores=scores)

