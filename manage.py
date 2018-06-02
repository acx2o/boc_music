from __future__ import print_function

from flaskr import app
app.run(host='127.0.0.1', port=5000, debug=True)

from flask_sqlalchemy import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flaskr import app, db

manager = Manager(app)

@manager.command
def init_db():
    print("=========================")
    db.create_all()

if __name__ == '__main__':
    print("=========================")
    manager.run()
