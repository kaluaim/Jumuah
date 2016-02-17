# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginEmailForm(Form):
    email = TextField('البريد الإلكتروني', [DataRequired(), Email()])
    password = PasswordField('كلمة المرور', [DataRequired()])


class LoginMobileForm(Form):
    country_code = TextField(
        'رمز الدولة',
        validators=[DataRequired(), Length(min=1, max=5)]
    )
    phone = TextField(
        'الجوال',
        validators=[DataRequired(), Length(min=9, max=9)]
    )


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
    otp_num = TextField(
        'رمز التحقق',
        validators=[DataRequired(), Length(min=4, max=4)]
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
    latitude = TextField(
        'خط الطول'
    )
    longitude = TextField(
        'خط العرض'
    )
    imam_name = TextField(
        'اسم الخطيب'
    )
    khutbah_start_time = TextField(
        'وقت بداية الخطبة'
    )
    khutbah_lenth = TextField(
        'مدة الخطبة'
    )
    has_chair_for_elderly = BooleanField(
        'وجود كرسي لكبار السن'
    )
    has_morgue = BooleanField(
        'وجود مغسلة اموات '
    )



class CreateTopic(Form):
    title = TextField('العنوان', validators=[DataRequired()])
