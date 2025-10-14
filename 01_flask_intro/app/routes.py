from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Kagan'}
    posts = [
        {
            'author': {'username': 'Ahmet'},
            'body': 'Beautiful day in Samsun!'
        },
        {
            'author': {'username': 'Hami'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)