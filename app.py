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

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:fgDSurwDPq5pwpJjt9q5@localhost/elpololito"
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
app.config["JWT_SECRET_KEY"] = "132iunfoiew09j3209d213mlkmzcpkcv0w3ir092k3mfppmzxclm03e92191CHAN"  

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
            "msg": "Usuario ingresado no esta registrado"
        })
    
    if  verifyPassword(dbuser.user_passwd, pwrd) is True:
        access_token = create_access_token(identity=dbuser)
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


@app.route("/password-recovery", methods=['POST'])
def recovery():
    user = request.json.get("mail")
    print(user)
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

@app.route("/get-user-info")
@jwt_required()
def userInfo():
    info=[]
    current_user = get_jwt_identity()
    results = db.session.query(Person,User).join(User).filter_by(user_id=current_user).all()
    for person, user in results:
        info.append({"name":person.person_fname,
                     "id":user.user_id,
                     "mail":user.user_email})
    return jsonify(info)

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
    resp["msg"] = f"Usuario {person.person_fname} creado con exito"
    resp["error"] = ""
    return jsonify(resp)


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



        
 
#Mati's code

@app.route("/get-workers", methods=['GET'])
def workers():
    workersList = []
    results = db.session.query(Person, User, Pololito, Publication).select_from(Person).join(User).join(Pololito).join(Publication).all()
    for person, user, pololito, publication in results:
        workersList.append({
            "Worker_id":pololito.fk_user_id,
            "name": person.person_fname,
            "last": person.person_lname,
            "mail": user.user_email,
            "pololito": pololito.pololito_id,
            "Title":publication.publication_title,
            "poster_id":publication.fk_user_id
        })

    return jsonify(workersList)


@jwt.user_identity_loader
def user_identity_lookup(tokenUser):
    return tokenUser.user_id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(user_id=identity).one_or_none()


@app.route("/home", methods=["GET"])
@jwt_required()
def home():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200



resp2 = {
    "id": "",
    "email" : ""
}   

@app.route("/who_am_i", methods=["GET"])
@jwt_required()

def whoami():
   
   return jsonify(      
        username=current_user.user_email,
        id=current_user.user_id
    )

@app.route("/create-pololito", methods=['POST'])
def CreatePololito():

    pololito = Pololito()
    rating = "1"
    pololito.pololito_rating = rating
    pololito.pololito_status = request.json.get("status")
    pololito.fk_user_id = request.json.get("user_id")
    pololito.fk_publication_id = request.json.get("pub_id")
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
