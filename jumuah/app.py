# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_bootstrap import Bootstrap
from flask.ext.bcrypt import Bcrypt
from flask.ext.googlemaps import GoogleMaps
import nexmo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../jumuah.db'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u"فضلاً قم بتسجيل الدخول."
login_manager.login_message_category = "info"
bootstrap = Bootstrap(app)
GoogleMaps(app)
nexmo = nexmo.Client(key='742ebb74', secret='a273d2d8')
