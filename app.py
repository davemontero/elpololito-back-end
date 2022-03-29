import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import current_user
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies


from itsdangerous import Serializer
from models import Professions, db, User, Person, Publication
from hash import verifyPassword, hashPassword
from validate import email_check, password_check

BASEDIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:luffy@localhost/elpololito"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_SECRET_KEY"] = "chanchanchan8w4erg874wbvf89w7bv87bwv2398hf983hn98evb2198743knmik"  
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
        token["token"] = create_access_token(identity=dbuser)
        token["user_id"] = dbuser.user_id
        return jsonify(resp, token )
        
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

lista = []
@app.route("/create-publication", methods=['POST','GET'])
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
    results = db.session.query(Person, User, Professions).select_from(Person).join(User).join(Professions)

    for person, professions in results:
        return jsonify(person.person_id, person.person_fname, person.person_lname, person.person_photo, professions.profession_name)


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





@app.route("/who_am_i", methods=["GET"])
@jwt_required()
def protected():

    results = db.session.query(Person, User).select_from(Person).join(User).filter(User.user_id == current_user.user_id).first()
    
    return jsonify(
        name=results.person.person_fname,
        id=current_user.user_id,
        email=current_user.user_email,  
    )

if __name__ == "__main__":
    app.run(host="localhost",port="3000")