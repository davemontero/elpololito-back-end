import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Person, User

BASEDIR = os.path.abspath(os.path.dirname(__file__))
dbname = 'elpololito.db'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASEDIR, dbname)}"
Migrate(app, db, render_as_batch=True)
db.init_app(app)
CORS(app)

@app.route("/login", methods=["GET"])
def login():
    user = request.json.get("user")
    pswd = request.json.get("password")
    dbpass = User.query.filter_by(umail=user).first()
    if pswd == dbpass.upass:
        return jsonify("Puede ingresar")

@app.route("/create-user", methods=['POST'])
def create_person():
    user = Person()
    user.pfname  = request.json.get("pfname")
    user.psname  = request.json.get("psname")
    user.plname  = request.json.get("plname")
    user.plname2 = request.json.get("plname2")
    user.prut    = request.json.get("prut")
    user.pphone  = request.json.get("pphone")
    user.pdob    = request.json.get("pdob")
    user.pgender = request.json.get("pgender")
    user.pphoto  = request.json.get("pphoto")

    db.session.add(user)
    db.session.commit()

    return user.serialize()


if __name__ == "__main__":
    app.run(host="localhost")