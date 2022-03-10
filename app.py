import json
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

@app.route("/create-user", methods=['POST'])
def create_user():
    user = User()
    user.umail  = request.json.get("mail")
    user.upass  = request.json.get("password")
    user.person_id = request.json.get("pid")

    db.session.add(user)
    db.session.commit()

    return user.serialize()

@app.route("/login")
def login():
    user = request.json.get("user")
    pwrd = request.json.get("password")
    dbuser = User.query.filter_by(umail=user).first()
    if pwrd == dbuser.upass:
        return jsonify("Inicio exitoso")
    else:
        return jsonify("Usuario o clave erronea")


@app.route("/password-recovery")
def recovery():
    user = request.json.get("mail")
    exist = User.query.filter_by(umail=user).first()
    
    if exist:
        return jsonify("Se enviara correo de recuperación")
    else:
        return jsonify("Usuario ingresado no posee cuenta")

if __name__ == "__main__":
    app.run(host="localhost")