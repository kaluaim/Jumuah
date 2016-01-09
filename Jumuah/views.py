from flask import render_template, redirect, url_for, request, flash
from app import app, db, login_manager
from forms import LoginForm, RegisterForm, AddMosqueForm
from flask.ext.login import login_user, logout_user, login_required
from models import User

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('You are logged in, welcome', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email and/or password', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            password=form.password.data,
            email=form.email.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Thank you for registering.', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You were logged out. Bye!', 'success')
    return redirect(url_for('index'))


@app.route('/mosque/')
@app.route('/mosque/<int:mosque_id>/')
def mosque(mosque_id=-1):
    if mosque_id is not -1:
        return render_template('mosque.html', id=mosque_id)
    else:
        return render_template('mosques.html')


@app.route('/mosque/add/', methods=['GET', 'POST'])
@login_required
def add_mosque():
    form = AddMosqueForm(request.form)
    return render_template('mosque_add.html', form=form)


@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500
