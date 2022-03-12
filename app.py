import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from models import db, User, Person
from hash import verifyPassword, hashPassword

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
    user.upass  = hashPassword(request.json.get("password"))
    user.person_id = request.json.get("pid")

    db.session.add(user)
    db.session.commit()

    return user.serialize()

@app.route("/login")
def login():
    user = request.json.get("user")
    pwrd = request.json.get("password")
    dbuser = User.query.filter_by(umail=user).first()
    if verifyPassword(dbuser.upass, pwrd) is True:
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


@app.route("/reset-password/<int:id>", methods=['PUT'])
def resetPassword(id):
    dbuser = User.query.filter_by(uid=id).first()
    dbuser.upass = hashPassword(request.json.get("password"))
    db.session.commit()
    return True

@app.route("/create-person", methods=['POST'])
def createPerson():
    person = Person()
    pdob = datetime.strptime(request.json.get("dob"), '%Y-%m-%d')
    person.pfname = request.json.get("fname")
    person.psname = request.json.get("sname")
    person.plname = request.json.get("lname")
    person.plname2 = request.json.get("lname2")
    person.prut = request.json.get("rut")
    person.pphone = request.json.get("phone")
    person.pdob = pdob.date()
    person.pgender = request.json.get("gender")

    db.session.add(person)
    db.session.commit()

    return person.serialize()

if __name__ == "__main__":
    app.run(host="localhost")