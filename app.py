import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import datetime
from models import db, User, Person
from hash import verifyPassword, hashPassword
from validate import email_check, password_check

BASEDIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
<<<<<<< HEAD
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:Ae18957319@localhost/elpololito"
=======
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:luffy@localhost/elpololito"
app.config["JWT_SECRET_KEY"] = "chanchanchan"  
jwt = JWTManager(app)
>>>>>>> 442b43378621fdafff6d1288675579d37e6ef7b6
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
        resp["msg"] = "Inicio exitoso"
        resp["error"] = ""
        resp["status"] = True
        access_token = create_access_token(identity=user.id)
        return jsonify(resp, { "token": access_token, "user_id": user.id })
        
    else: 
        resp["status"] = False
        resp["msg"] = "Usuario o contraseña incorrecto"
        resp["error"] = "Usuario o contraseña incorrecto"
        return jsonify(resp)


@app.route("/password-recovery",methods=['POST'])
def recovery():
    user = request.json.get("mail")
    ucheck = email_check(user)

    if ucheck is False:
        resp["status"] = False
        resp["msg"]= "Favor, ingresar un correo valido"
        return jsonify(resp)

    exist = User.query.filter_by(user_email=user).first()

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
<<<<<<< HEAD
    person.pfname = request.json.get("fname")
    person.psname = request.json.get("sname")
    person.plname = request.json.get("lname")
    person.plname2 = request.json.get("lname2")
    person.prut = request.json.get("rut")
    person.pphone = request.json.get("phone")
    person.pdob = pdob.date()
    person.pgender = request.json.get("gender")
    person.pphoto = request.json.get("photo")
=======
    person.person_fname = request.json.get("fname")
    person.person_sname = request.json.get("sname")
    person.person_lname = request.json.get("lname")
    person.person_lname2 = request.json.get("lname2")
    person.person_rut = request.json.get("rut")
    person.person_phone = request.json.get("phone")
    person.person_dob = pdob.date()
    person.person_gender = request.json.get("gender")
>>>>>>> 442b43378621fdafff6d1288675579d37e6ef7b6

    db.session.add(person)
    db.session.commit()

    return person.serialize()

if __name__ == "__main__":
    app.run(host="localhost")