from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Person(db.Model):
    person_id     = db.Column(db.Integer, primary_key=True)
    person_fname  = db.Column(db.String(50), nullable=False)
    person_sname  = db.Column(db.String(50))
    person_lname  = db.Column(db.String(50), nullable=False)
    person_lname2 = db.Column(db.String(50))
    person_rut    = db.Column(db.Integer, nullable=False, unique=True)
    person_phone  = db.Column(db.Integer)
    person_dob    = db.Column(db.Date, nullable=False)
    person_gender = db.Column(db.String(10))
    person_photo  = db.Column(db.String(50))
    create_at     = db.Column(db.DateTime, default=datetime.now())
    user          = db.relationship('User', backref='person', lazy=True)

    def __repr__(self):
        return f"<Person {self.person_id}>"
    
    def serialize(self):
        return {
            "pid": self.pid,
            "fullname": f"{self.pfname} {self.plname}"
        }

class User(db.Model):
    user_id         = db.Column(db.Integer, primary_key=True)
    user_email      = db.Column(db.String(120), unique=True, nullable=False)
    user_passwd     = db.Column(db.String(120), nullable=False)
    create_at       = db.Column(db.DateTime, default=datetime.now())
    fk_person_id    = db.Column(db.Integer, db.ForeignKey('person.pid'), nullable=False)

    def __repr__(self):
        return f"<User {self.user_id}>"

    def serialize(self):
        return {
            "mail": self.umail,
            "pass": self.upass
        }

class publication(db.Model):
    publication_id      = db.Column(db.Integer, primary_key=True)
    publication_desc    = db.Column(db.Text(1000), nullable=False)
    publication_place   = db.Column(db.String(50), nullable=True)
    create_at           = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"<Publication {self.publication_id}>"

class Pololito(db.Model):
    pololito_id = db.Column(db.Integer, primary_key=True)
    pololito_rating  = db.Column(db.Enum('1','2','3','4','5'), nullable=True)
    pololito_status  = db.Column(db.String())
    create_at           = db.Column(db.DateTime, default=datetime.now())