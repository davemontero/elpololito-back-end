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
from hash import verifyPassword, hashPassword, get_random_password
from mail import recovery_mail
from validate import email_check, password_check

BASEDIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:fgDSurwDPq5pwpJjt9q5@localhost/elpololito"
app.config["JWT_SECRET_KEY"] = "chanchanchan"  
jwt = JWTManager(app)
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
        return jsonify({
            "status": False,
            "msg": "Ingresar un correo valido"
        })
        
    if pcheck["val"] is False:
        return jsonify({
            "status": False,
            "msg": "Usuario o contraseña incorrecto"
        })
    
    dbuser = User.query.filter_by(user_email=user).first()
    
    if not dbuser:
        return jsonify({
            "status": False,
            "msg": "Usuarios ingresado no esta registrado"
        })
    
    if  verifyPassword(dbuser.user_passwd, pwrd) is True:
        user = User()
        access_token = create_access_token(identity=user.user_id)
        return jsonify({
            "status": True,
            "msg": "Inicio exitoso",
            "token": access_token
            })
    else: 
        return jsonify({
            "status": False,
            "msg": "Usuario o contraseña incorrecto"
        })


@app.route("/password-recovery",methods=['POST'])
def recovery():
    user = request.json.get("mail")
    ucheck = email_check(user)

    if ucheck is False:
        return jsonify({
            "status": False,
            "msg": "Ingresar un correo valido"
        })

    exist = User.query.filter_by(user_email=user).first()

    if exist:
        new_pass = get_random_password()
        exist.user_passwd = hashPassword(new_pass)
        db.session.commit()
        if recovery_mail(user,new_pass) is True:
            return jsonify({
                "status": True,
                "msg": "Se enviará correo de recuperación"
            })
    else:
        return jsonify({
            "status": False,
            "msg": "Correo ingresado no posee cuenta"
        })

@app.route("/reset-password", methods=['PUT'])
def resetPassword():
    
    user = request.json.get("mail")
    old = request.json.get("old_password")
    new = request.json.get("new_password")
    dbUser = User.query.filter_by(user_email=user).first()

    if verifyPassword(dbUser.user_passwd, old) is True:
        dbUser.user_passwd = hashPassword(new)
        db.session.commit()
        return jsonify({
            "status": True,
            "msg": "Se ha modificado la contraseña correctamente"
        })
    else:
        return jsonify({
            "status": False,
            "msg": "La contraseña actual ingresada es incorrecta"
        })

@app.route("/create-person", methods=['POST'])
def createPerson():
    person = Person()
    user = User()
    pdob = datetime.strptime(request.json.get("dob"), '%Y-%m-%d')
    person.person_fname = request.json.get("fname")
    person.person_sname = request.json.get("sname")
    person.person_lname = request.json.get("lname")
    person.person_lname2 = request.json.get("lname2")
    person.person_rut = request.json.get("rut")
    person.person_phone = request.json.get("phone")
    person.person_dob = pdob.date()
    person.person_gender = request.json.get("gender")


    ucheck = email_check(request.json.get("mail"))
    pcheck = password_check(request.json.get("password"))

    if ucheck is False:
        resp["status"] = False
        resp["msg"]= "Favor, ingresar un correo valido"
        return jsonify(resp)
    
    if pcheck["val"] is False:
        resp["status"] = False
        resp["msg"] = "La contraseña no cumple con lo establecido"
        resp["error"] = pcheck["msg"]
        return jsonify(resp)

    db.session.add(person)
    db.session.flush()
    db.session.refresh(person)

    user.user_email = request.json.get("mail")
    user.user_passwd  = hashPassword(request.json.get("password"))
    user.fk_person_id = person.person_id
    db.session.add(user)
    db.session.commit()

    return person.serialize()

if __name__ == "__main__":
    app.run(host="localhost",port="3000")