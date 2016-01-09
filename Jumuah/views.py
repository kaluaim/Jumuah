from flask import render_template, redirect, url_for
from app import app

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/register/')
def register():
    return render_template('register.html')


@app.route('/logout/')
def logout():
    return redirect(url_for('index'))


@app.route('/mosque/')
@app.route('/mosque/<int:mosque_id>/')
def mosque(mosque_id=-1):
    if mosque_id is not -1:
        return render_template('mosque.html', id=mosque_id)
    else:
        return render_template('mosques.html')


@app.route('/mosque/add/')
def add_mosque():
    return render_template('mosques.html')
