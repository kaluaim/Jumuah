from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(Form):
    email = TextField('Email Address', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])


class RegisterForm(Form):
    email = TextField(
        'Email Address',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Confirm password',
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
