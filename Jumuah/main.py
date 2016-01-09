from app import app, db
from views import *

db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=8088)
