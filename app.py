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
    

    person.pfname = pfname
    person.psname = psname
    person.plname = plname
    person.plname2 = plname2
    person.prut = prut
    person.pphone = pphone
    person.pdob = pdob.date()
    person.pgender = pgender
    person.pphoto = pphoto


    db.session.add(person)
    db.session.commit()

    return jsonify(person.serialize()), 200


if __name__ == "__main__":
    app.run(host="localhost",port="3000")