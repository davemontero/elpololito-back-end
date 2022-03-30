import os
from unittest import result
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required, current_user
from datetime import datetime
from models import Pololito, Professions, db, User, Person, Publication
from hash import verifyPassword, hashPassword, get_random_password
from validate import email_check, password_check
from mail import recovery_mail

BASEDIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
<<<<<<< HEAD
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:Ae18957319@localhost/elpololito"
=======
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:root@localhost/elpololito"
>>>>>>> 8427b82514e1dca1b2ebbe12da1316516737c572
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
token = {
    "token": "",
    "user_id": ""
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
        resp["msg"] = "Favor, ingresar un correo valido"
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

    if verifyPassword(dbuser.user_passwd, pwrd) is True:
        resp["msg"] = "Inicio exitoso"
        resp["error"] = ""
        resp["status"] = True
        token["token"] = create_access_token(identity=dbuser)
        token["user_id"] = dbuser.user_id
        return jsonify(resp, token)

    else:
        resp["status"] = False
        resp["msg"] = "Usuario o contraseña incorrecto"
        resp["error"] = "Usuario o contraseña incorrecto"
        return jsonify(resp)


@app.route("/password-recovery", methods=['POST'])
def recovery():
    user = request.json.get("mail")
    ucheck = email_check(user)

    if ucheck is False:
        resp["status"] = False
        resp["msg"] = "Favor, ingresar un correo valido"
        return jsonify(resp)

    exist = User.query.filter_by(user_email=user).first()

    if exist:
        new_pass = get_random_password()
        exist.user_passwd = hashPassword(new_pass)
        db.session.commit()
        if recovery_mail(user,new_pass) is True:
            resp["status"] = True
            resp["msg"] = "Se ha enviado correo de recuperación con su nueva contraseña"
            return jsonify(resp)
        else:
            resp["status"] = False
            resp["msg"] = "¡Ups! parece que ha ocurrido un error"
            return jsonify(resp)
    else:
        resp["status"] = False
        resp["msg"] = "Correo ingresado no posee cuenta"
        return jsonify(resp)


@app.route("/reset-password", methods=['PUT'])
def resetPassword():
    user = request.json.get("mail")
    old = request.json.get("old_password")
    new = request.json.get("new_password")
    dbUser = User.query.filter_by(user_email=user).first()
    if verifyPassword(dbUser.user_passwd, old) is True:
        dbUser.user_passwd = hashPassword(new)
        db.session.commit()
        resp["status"] = True
        resp["msg"] = "Se ha modificado la contraseña correctamente"
        return jsonify(resp)
    else:
        resp["status"] = False
        resp["msg"] = "Contraseña incorrecta"




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

    rut_exist = Person.query.filter_by(
        person_rut=request.json.get("rut")).first()

    if rut_exist:
        resp["status"] = False
        resp["msg"] = "El RUT ingresado ya existe"
        return jsonify(resp)

    ucheck = email_check(request.json.get("mail"))
    pcheck = password_check(request.json.get("password"))

    if ucheck is False:
        resp["status"] = False
        resp["msg"] = "Favor, ingresar un correo valido"
        return jsonify(resp)

    if pcheck["val"] is False:
        resp["status"] = False
        resp["msg"] = "La contraseña no cumple con lo establecido"
        resp["error"] = pcheck["msg"]
        return jsonify(resp)

    user.user_email = request.json.get("mail")
    email_exist = User.query.filter_by(
        user_email=request.json.get("mail")).first()
    if email_exist:
        resp["status"] = False
        resp["msg"] = "El correo ingresado ya existe"
        return jsonify(resp)

    db.session.add(person)
    db.session.flush()
    db.session.refresh(person)
    user.user_passwd = hashPassword(request.json.get("password"))
    user.fk_person_id = person.person_id
    db.session.add(user)
    db.session.commit()
    resp["status"] = True
    resp["msg"] = "Usuario creado con exito"
    resp["error"] = ""
    return jsonify(resp)

    return person.serialize()

@app.route("/create-publication", methods=['POST', 'GET'])
def publication():

    if request.method == 'POST':
        publication = Publication()
        publication.publication_desc = request.json.get("body")
        publication.publication_place = request.json.get("address")
        publication.publication_title = request.json.get("title")
        publication.fk_user_id = request.json.get("user_id")

        db.session.add(publication)
        db.session.flush()
        db.session.refresh(publication)
        db.session.commit()

        return jsonify("Exito")

    if request.method == 'GET':
        publications = Publication.query.all()
        toReturn = [publication.serialize() for publication in publications]
        return jsonify(toReturn), 200


<<<<<<< HEAD

        
 
#Mati's code
=======
# Mati's code
>>>>>>> 8427b82514e1dca1b2ebbe12da1316516737c572

@app.route("/get-workers", methods=['GET'])
def workers():
    workersList = []
    results = db.session.query(Person, User, Publication, Pololito).select_from(Person).join(User).join(Publication).join(Pololito).all()
    for person, user, publication, pololito in results:
        workersList.append({
            "person_id": person.person_id,
            "name": person.person_fname,
            "last": person.person_lname,
            "user_id": user.user_id,
            "mail": user.user_email,
            "publication": publication.publication_title,
            "pololito": pololito.pololito_id
        })

    return jsonify(workersList)


@jwt.user_identity_loader
def user_identity_lookup(dbuser):
    return dbuser.user_id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(user_id=identity).one_or_none()


@app.route("/home", methods=["GET"])
@jwt_required()
def home():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

<<<<<<< HEAD



=======
resp2 = {
    "id": "",
    "email": ""
}
>>>>>>> 8427b82514e1dca1b2ebbe12da1316516737c572

@app.route("/who_am_i", methods=["GET"])
def protected():
<<<<<<< HEAD

     
    
    return jsonify(
        id=current_user.user_id,
        email=current_user.user_email 
              
    )
=======
    results = db.session.query(Person, User, Publication, Pololito).select_from(Person).join(User).join(Publication).join(Pololito).all()
    return jsonify("testing")
>>>>>>> 8427b82514e1dca1b2ebbe12da1316516737c572

@app.route("/create-pololito", methods=['POST'])
def CreatePololito():

    pololito = Pololito()
<<<<<<< HEAD
    pololito.fk_user_id=request.json.get("user_id")
    pololito.fk_publication_id=request.json.get("pub_id")
=======
    rating = "1"
    pololito.pololito_rating = rating
    pololito.pololito_status = request.json.get("status")
    pololito.fk_user_id = request.json.get("user_id")
    pololito.fk_publication_id = request.json.get("pub_id")
>>>>>>> 8427b82514e1dca1b2ebbe12da1316516737c572
    db.session.add(pololito)
    db.session.commit()
    return jsonify("Felicidades por su pololito exito")

@app.route("/test", methods=['GET'])
def consulta():
    workers = db.session.query(Person, User, Publication, Pololito).select_from(Person).join(User).join(Publication).join(Pololito).all()
    toReturnUser = list(map(lambda user:user.serialize(),workers))
    print (workers)
    return jsonify(
            user = toReturnUser,
            )


if __name__ == "__main__":
    app.run(host="localhost", port="3000")
