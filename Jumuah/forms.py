# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(Form):
    email = TextField('البريد الإلكتروني', [DataRequired(), Email()])
    password = PasswordField('كلمة المرور', [DataRequired()])


class RegisterForm(Form):
    email = TextField(
        'البريد الإلكتروني',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        'كلمة المرور',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'تأكيد كلمة المرور',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )


class AddMosqueForm(Form):
    name = TextField(
        'Mosque Name',
        validators=[DataRequired()]
    )
    country = TextField(
        'Country',
        validators=[DataRequired()]
    )
    province = TextField(
        'Province',
        validators=[DataRequired()]
    )
    city = TextField(
        'City',
        validators=[DataRequired()]
    )
    district = TextField(
        'district',
        validators=[DataRequired()]
    )


class CreateTopic(Form):
    title = TextField('Title', validators=[DataRequired()])
