import sys
reload(sys)
sys.setdefaultencoding('utf8')

from app import app, db
from models import *
from views import *

db.create_all()
db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=8083)
