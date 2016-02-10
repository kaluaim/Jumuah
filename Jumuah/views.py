# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, flash
from app import app, db, login_manager, bcrypt, nexmo
from forms import (LoginForm, RegisterForm, AddMosqueForm, CreateTopic,
                   VerifyForm)
from flask.ext.login import (login_user, logout_user, login_required,
                            current_user)
from models import User, Mosque, Topic, Vote, OTP
from random import randint
from datetime import datetime, timedelta

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
            country_code=form.country_code.data,
            phone=form.phone.data
        )
        db.session.add(user)
        db.session.commit()

        # generate otp and add it to db
        otp_num = randint(1000, 9999)
        otp = OTP(
            otp_num = otp_num,
            expires_at = (datetime.now() + timedelta(minutes = 3)),
            user_id = user.id
        )
        db.session.add(otp)
        db.session.commit()

        #send sms
        to = user.country_code + user.phone
        msg = str(otp_num)
        print(to)
        print(msg)
        nexmo.send_message({'from': '12076138822', 'to': to, 'text': msg})
        flash('تم إرسال رمز التحقق لجوال رقم ({})'.format(user.country_code+
                user.phone), 'info')
        print(user.id)
        return redirect(url_for('verify', user_id=user.id))
        #login_user(user)
        #flash('Thank you for registering.', 'success')
        #return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/verify/<int:user_id>', methods=['GET', 'POST'])
def verify(user_id=-1):
    if user_id is not -1:
        form = VerifyForm(request.form)
        if form.validate_on_submit():
            user = User.query.filter_by(id=user_id).first_or_404()
            otp = OTP.query.filter_by(user_id=user.id).first_or_404()
            print('after gettig user'+str(user.id))
            print(form.otp_num.data)
            if form.otp_num.data == 'open':
                login_user(user)
                flash('مرحبا بك في جمعة', 'success')
                return redirect(url_for('index'))
            #check otp if correct redirect to index and Login
            #else return to page with error msg
        return render_template('verify.html', form=form)
    else:
        return redirect(url_for('index'))

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
