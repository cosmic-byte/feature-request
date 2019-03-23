import flask
from flask import Blueprint, url_for, render_template, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import redirect

from app import flask_bcrypt, db
from app.auth.auth_helper import is_safe_url
from app.auth.forms import LoginForm
from app.auth.model import User
from app.util import save_changes

app = Blueprint('auth', __name__, template_folder='templates',
                static_folder='static')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """For GET requests, display the login form.
    For POSTS, login the current user by processing the form.

    """
    form = LoginForm(formdata=request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if flask_bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                save_changes(db.session)
                login_user(user, remember=True)

                next_page = flask.request.args.get('next')
                if not is_safe_url(next_page):
                    return flask.abort(400)

                return redirect(next_page or url_for('home.home'))
    if current_user and current_user.is_authenticated:
        return redirect(url_for('home.home'))
    return render_template('forms/login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    save_changes(db.session)
    logout_user()
    return redirect(url_for('auth.login'))
