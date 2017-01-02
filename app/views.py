from flask import render_template
from app import app

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
