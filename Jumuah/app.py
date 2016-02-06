# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_bootstrap import Bootstrap
from flask.ext.bcrypt import Bcrypt
from twilio.rest import TwilioRestClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jumuah.db'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u"فضلاً قم بتسجيل الدخول."
login_manager.login_message_category = "info"
bootstrap = Bootstrap(app)
account = "ACcb954786d23cb5d29c6987c381ac824c"
token = "4149752b6735f9dd8ce79a268b524ce6"
twilio = TwilioRestClient(account, token)
