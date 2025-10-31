from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm
from app.forms import ForgetPasswordForm


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


@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        return redirect(url_for('login'))
    return render_template('forget_password.html', title='Forget Password', form=form)