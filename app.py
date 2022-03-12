import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Person
from datetime import datetime

BASEDIR = os.path.abspath(os.path.dirname(__file__))
dbname = 'elpololito.db'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASEDIR, dbname)}"
Migrate(app, db, render_as_batch=True)
db.init_app(app)
CORS(app)

@app.route("/people", methods=["POST"])
def create_person():
    person = Person()
    pfname = request.json.get("pfname")
    psname = request.json.get("psname")
    plname = request.json.get("plname")
    plname2 = request.json.get("plname2")
    prut = request.json.get("prut")
    pphone = request.json.get("pphone")
    pdob = datetime.strptime(request.json.get("pdob"), '%Y-%m-%d')
    pgender = request.json.get("pgender")
    pphoto = request.json.get("pphoto")
    
    if type(pfname) != str:
        return jsonify({
            "msg":"El nombre debe ser tipo string"
        }), 400
        
    if type(psname) != str:
        return jsonify({
            "msg":"El segundo nombre debe ser tipo string"
        }), 400

    if type(plname) != str:
        return jsonify({
            "msg":"El apellido paterno debe ser tipo string"
        }), 400

    if type(plname2) != str:
        return jsonify({
            "msg":"El apellido materno debe ser tipo string"
        }), 400

    if type(pgender) != str:
        return jsonify({
            "msg":"El genero debe ser tipo string"
        }), 400

    if len(pfname)<1:
        return jsonify({
            "msg":"El nombre no puede estar vacio o debe tener al menos 1 caracter"
        }), 400
    if len(psname)<1:
        return jsonify({
            "msg":"El nombre no puede estar vacio o debe tener al menos 1 caracter"
        }), 400
    if len(plname)<1:
        return jsonify({
            "msg":"El nombre no puede estar vacio o debe tener al menos 1 caracter"
        }), 400
    if len(plname2)<1:
        return jsonify({
            "msg":"El nombre no puede estar vacio o debe tener al menos 1 caracter"
        }), 400
    if len(pgender)<1 or len(pgender)<2:
        return jsonify({
            "msg":"El nombre no puede estar vacio o debe tener al menos 1 caracter"
        }), 400
    
    

    person.pfname = pfname.strip()
    person.psname = psname
    person.plname = plname
    person.plname2 = plname2
    person.prut = prut
    person.pphone = pphone
    person.pdob = pdob
    person.pgender = pgender
    person.pphoto = pphoto

    db.session.add(person)
    db.session.commit()

    return jsonify(person.serialize()), 200


if __name__ == "__main__":
    app.run(host="localhost",port="3000")