from app import app, db
from models import User
from views import *

db.create_all()
db.session.add(User("khalid", "khalidpassword", "kalid@email.com"))
db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=8088)
