from flask import Blueprint, g, render_template
from flaskr.auth import login_required

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/landing')
@login_required
def landing():
    fav_team = g.user['fav_team']
    return render_template('user/landing.html', fav_team=fav_team)
