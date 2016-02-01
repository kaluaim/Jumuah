# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, flash
from app import app, db, login_manager, bcrypt
from forms import LoginForm, RegisterForm, AddMosqueForm, CreateTopic
from flask.ext.login import (login_user, logout_user, login_required,
                            current_user)
from models import User, Mosque, Topic, Vote

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash,
                    form.password.data):
            login_user(user)
            flash('تم تسجيل دخولك بنجاح', 'success')
            return redirect(url_for('index'))
        else:
            flash('خطاء بتسجيل الدخول', 'danger')
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
@app.route('/mosque/<int:mosque_id>/', methods=['GET'])
def mosque(mosque_id=-1):
    if mosque_id is not -1:
        form = CreateTopic(request.form)
        mosque = Mosque.query.filter_by(id=mosque_id).first_or_404()
        return render_template('mosque.html', mosque=mosque, form=form)
    else:
        mosques = Mosque.query.all()
        return render_template('mosques.html/', mosques=mosques)

@app.route('/mosque/add/', methods=['GET', 'POST'])
@login_required
def add_mosque():
    form = AddMosqueForm(request.form)
    if form.validate_on_submit():
        mosque = Mosque(
            name=form.name.data,
            country=form.country.data,
            province=form.province.data,
            city=form.city.data,
            district=form.district.data
        )
        db.session.add(mosque)
        db.session.commit()
        flash('تم إضافة الجامع بنجاح.', 'success')
        return redirect(url_for('mosque'))
    return render_template('mosque_add.html', form=form)

@app.route('/mosque/<int:mosque_id>/topic/', methods=['POST'])
@login_required
def add_topic(mosque_id=-1):
    if mosque_id is not -1:
        form = CreateTopic(request.form)
        if form.validate_on_submit():
            topic = Topic(
                title=form.title.data,
                user_created_id=current_user.id,
                mosque_id=mosque_id
            )
            db.session.add(topic)
            db.session.commit()
            flash('تم إضافة الموضوع بنجاح.', 'success')
        return redirect(url_for('mosque', mosque_id=mosque_id))
    else:
        mosques = Mosque.query.all()
        return render_template('mosques.html/', mosques=mosques)

@app.route('/mosque/<int:mosque_id>/<int:topic_id>/vote/', methods=['GET'])
@login_required
def vote(mosque_id=-1, topic_id=-1):
    if mosque_id is not -1 and topic_id is not -1:
        vote = Vote(
            topic_id=topic_id,
            user_id=current_user.id,
        )
        db.session.add(vote)
        db.session.commit()
        flash('vote added', 'success')
    return redirect(url_for('mosque', mosque_id=mosque_id))

@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500
