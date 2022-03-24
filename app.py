import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from models import db, User, Person
from hash import verifyPassword, hashPassword
from validate import email_check, password_check
from mail import recovery_mail

BASEDIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:fgDSurwDPq5pwpJjt9q5@localhost/elpololito"
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
    
    dbuser = User.query.filter_by(user_email=user).first()
    
    if not dbuser:
        resp["status"] = False
        resp["msg"] = "Usuario ingresado no esta registrado"
        resp["error"] = "Usuario ingresado no esta registrado"
        return jsonify(resp)
    
    if  verifyPassword(dbuser.user_passwd, pwrd) is True:
        resp["status"] = True
        resp["msg"] = "Inicio exitoso"
        resp["error"] = ""
        return jsonify(resp)
    else: 
        resp["status"] = False
        resp["msg"] = "Usuario o contraseña incorrecto"
        resp["error"] = "Usuario o contraseña incorrecto"
        return jsonify(resp)

@app.route("/password-recovery", methods=["POST"])
def recovery():
    user = request.json.get("mail")
    print(user)
    ucheck = email_check(user)

    if ucheck is False:
        resp["status"] = False
        resp["msg"]= "Favor, ingresar un correo valido"
        return jsonify(resp)

    exist = User.query.filter_by(user_email=user).first()

    if exist:
        if recovery_mail(exist.user_email, exist.user_id) is True:
            resp["status"] = True
            resp["msg"] = "Correo enviado, revise su bandeja de entrada"
            return jsonify(resp)
    else:
        resp["status"] = False
        resp["msg"]= "Correo ingresado no posee cuenta"
        return jsonify(resp)

@app.route("/reset-password/<int:id>", methods=['PUT'])
def resetPassword(id):
    dbuser = User.query.filter_by(user_email=id).first()
    newPassword = request.json.get("password")

    pcheck = password_check(newPassword)
    if pcheck["val"] is False:
        resp["status"] = False
        resp["msg"] = "La contraseña no cumple con lo establecido"
        resp["error"] = pcheck["msg"]
        return jsonify(resp)

    dbuser.user_passwd = hashPassword(newPassword)
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

    user.user_email = umail
    user.user_passwd  = hashPassword(upass)
    user.fk_person_id = person_id

    db.session.add(user)
    db.session.commit()

    return user.serialize()

@app.route("/create-person", methods=['POST'])
def createPerson():
    person = Person()
    pdob = datetime.strptime(request.json.get("dob"), '%Y-%m-%d')
    person.person_fname = request.json.get("fname")
    person.person_sname = request.json.get("sname")
    person.person_lname = request.json.get("lname")
    person.person_lname2 = request.json.get("lname2")
    person.person_rut = request.json.get("rut")
    person.person_phone = request.json.get("phone")
    person.person_dob = pdob.date()
    person.person_gender = request.json.get("gender")

    db.session.add(person)
    db.session.commit()

    return person.serialize()

if __name__ == "__main__":
    app.run(host="localhost")