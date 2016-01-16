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
        'اسم الجامع',
        validators=[DataRequired()]
    )
    country = TextField(
        'الدولة',
        validators=[DataRequired()]
    )
    province = TextField(
        'المنطقة',
        validators=[DataRequired()]
    )
    city = TextField(
        'المدينة',
        validators=[DataRequired()]
    )
    district = TextField(
        'الحي',
        validators=[DataRequired()]
    )


class CreateTopic(Form):
    title = TextField('العنوان', validators=[DataRequired()])
