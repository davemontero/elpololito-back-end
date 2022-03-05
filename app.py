import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from models import db

BASEDIR = os.path.abspath(os.path.dirname(__file__))
dbname = 'elpololito.db'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASEDIR, dbname)}"
Migrate(app, db, render_as_batch=True)
db.init_app(app)
CORS(app)

if __name__ == "__main__":
    app.run(host="localhost")