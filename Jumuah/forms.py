# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(Form):
    email = TextField('البريد الإلكتروني', [DataRequired(), Email()])
    password = PasswordField('كلمة المرور', [DataRequired()])


class RegisterForm(Form):
    country_code = TextField(
        'رمز الدولة',
        validators=[DataRequired(), Length(min=1, max=5)]
    )
    phone = TextField(
        'الجوال',
        validators=[DataRequired(), Length(min=9, max=9)]
    )


class VerifyForm(Form):



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
