from flask import Blueprint, g, render_template
from flaskr.auth import login_required
from dotenv import load_dotenv
import os
from balldontlie import BalldontlieAPI

bp = Blueprint('user', __name__, url_prefix='/user')

# Load .env and initialize API
load_dotenv()
api = BalldontlieAPI(api_key=os.getenv("API_KEY"))

@bp.route('/landing')
@login_required
def landing():
    fav_team = g.user['fav_team']

    # Fetch roster for favorite team
    players = []
    teams_data = api.nba.teams.list()

    # Find the team id
    team_id = None
    for team in teams_data.data:
        if team.full_name.lower() == fav_team.lower():
            team_id = team.id
            break

    if team_id:
        # Now fetch players for that team
        players_data = api.nba.players.list(team_ids=[team_id])
        players = players_data.data

    return render_template('user/landing.html', fav_team=fav_team, players=players)
