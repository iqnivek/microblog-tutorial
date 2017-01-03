from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm
from .models import User

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Kevin'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The movie was cool.'
        }
    ]

    return render_template(
        'index.html',
        title='Home',
        user=user,
        posts=posts
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data

        email = form.email.data
        user = User.query.filter_by(email=email)
        user = User(nickname=email.split('@')[0], email=email)
        db.session.add(user)
        db.session.commit()

        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user, remember = remember_me)

        return redirect(url_for('index'))
    return render_template(
        'login.html',
        title='Sign in',
        form=form
    )
