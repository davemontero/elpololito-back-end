import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from models import db, User, Person
from hash import verifyPassword, hashPassword
from validate import email_check, password_check

BASEDIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:root@localhost/elpololito"
Migrate(app, db, render_as_batch=True)
db.init_app(app)
CORS(app)

resp = {
    "status": True,
    "msg": "",
    "error": ""
}

# Dave code
@app.route("/login", methods=['POST'])
def login():
    user = request.json.get("user")
    pwrd = request.json.get("password")

    ucheck = email_check(user)
    pcheck = password_check(pwrd)

    if ucheck is False:
        resp["status"] = False
        resp["msg"]= "Favor, ingresar un correo valido"
        return jsonify(resp)
    
    if pcheck["val"] is False:
        resp["status"] = False
        resp["msg"] = "Usuario o contraseña incorrecto"
        resp["error"] = pcheck["msg"]
        return jsonify(resp)

    dbuser = User.query.filter_by(umail=user).first()
    vp = verifyPassword(dbuser.upass, pwrd)
    if  vp:
        resp["msg"] = "Inicio exitoso"
        resp["error"] = ""
        resp["status"] = True
        return jsonify(resp)
    else: 
        resp["status"] = False
        resp["msg"] = "Usuario o contraseña incorrecto"
        resp["error"] = vp["e"]
        return jsonify(resp)

@app.route("/password-recovery")
def recovery():
    user = request.json.get("mail")
    ucheck = email_check(user)

    if ucheck is False:
        resp["status"] = False
        resp["msg"]= "Favor, ingresar un correo valido"
        return jsonify(resp)

    exist = User.query.filter_by(umail=user).first()

    if exist:
        resp["status"] = True
        resp["msg"]= "Se enviará correo de recuperación"
        return jsonify(resp)
    else:
        resp["status"] = False
        resp["msg"]= "Correo ingresado no posee cuenta"
        return jsonify(resp)

@app.route("/reset-password/<int:id>", methods=['PUT'])
def resetPassword(id):
    dbuser = User.query.filter_by(uid=id).first()
    newPassword = request.json.get("password")

    pcheck = password_check(newPassword)
    if pcheck["val"] is False:
        resp["status"] = False
        resp["msg"] = "La contraseña no cumple con lo establecido"
        resp["error"] = pcheck["msg"]
        return jsonify(resp)

    dbuser.upass = hashPassword(newPassword)
    db.session.commit()
    resp["check"] = True
    resp["msg"] = "Contraseña cambiada exitosamente"
    return jsonify(resp)

# Oscar's code
@app.route("/create-user", methods=['POST'])
def create_user():
    user = User()
    umail = request.json.get("mail")
    upass = request.json.get("password")
    person_id = request.json.get("pid")

    ucheck = email_check(umail)
    pcheck = password_check(upass)

    if ucheck is False:
        resp["status"] = False
        resp["msg"]= "Favor, ingresar un correo valido"
        return jsonify(resp)
    
    if pcheck["val"] is False:
        resp["status"] = False
        resp["msg"] = "La contraseña no cumple con lo establecido"
        resp["error"] = pcheck["msg"]
        return jsonify(resp)

    user.umail = umail
    user.upass  = hashPassword(upass)
    user.person_id = person_id

    db.session.add(user)
    db.session.commit()

    return user.serialize()

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