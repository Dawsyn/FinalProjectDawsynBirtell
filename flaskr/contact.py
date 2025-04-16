from flask import(
    Blueprint, render_template, request, redirect, url_for, flash
) 

from flaskr.db import get_db

bp = Blueprint('contact', __name__, url_prefix='/contact')

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Basic validation
        error = None
        if not name or not email:
            error = 'Name and Email are required.'
        
        if error is not None:
            flash(error)
        else:
            # Insert into DB
            db = get_db()
            db.execute(
                'INSERT INTO contact (name, email, message)'
                ' VALUES (?, ?, ?)',
                (name, email, message)
            )
            db.commit()

            return redirect(url_for('contact.index'))

    # If GET request or if there's an error, just render the page
    return render_template('contact/contact.html')