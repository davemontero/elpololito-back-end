from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

person_profession = db.Table('person_profession', 
    db.Column('fk_person_id', db.Integer, db.ForeignKey('person.person_id')), 
    db.Column('fk_profession_id', db.Integer, db.ForeignKey('professions.profession_id')))
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
    profession    = db.relationship('Professions', secondary=person_profession, back_populates='professional')
    

    def __repr__(self):
        return f"<Person {self.person_id}>"
    
    def serialize(self):
        return {
            "person_id": self.person_id,
            "fullname": f"{self.person_fname} {self.person_lname}"
        }

class User(db.Model):
    user_id         = db.Column(db.Integer, primary_key=True)
    user_email      = db.Column(db.String(120), unique=True, nullable=False)
    user_passwd     = db.Column(db.String(120), nullable=False)
    create_at       = db.Column(db.DateTime, default=datetime.now())
    fk_person_id    = db.Column(db.Integer, db.ForeignKey('person.person_id'), nullable=False)
    publication     = db.relationship('Publication', backref='user', lazy=True)
    pololito        = db.relationship('Pololito', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.user_id}>"

    def serialize(self):
        return {
            "mail": self.user_email,
            "pass": self.user_passwd
        }

class Publication(db.Model):
    publication_id      = db.Column(db.Integer, primary_key=True)
    publication_desc    = db.Column(db.Text(1000), nullable=False)
    publication_place   = db.Column(db.String(50), nullable=True)
    create_at           = db.Column(db.DateTime, default=datetime.now())
    fk_user_id          = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    def __repr__(self):
        return f"<Publication {self.publication_id}>"

class Pololito(db.Model):
    pololito_id         = db.Column(db.Integer, primary_key=True)
    pololito_rating     = db.Column(db.Enum('1','2','3','4','5'), nullable=True)
    pololito_status     = db.Column(db.Boolean, default=True, unique=False)
    create_at           = db.Column(db.DateTime, default=datetime.now())
    fk_user_id          = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    fk_publication_id   = db.Column(db.Integer, db.ForeignKey('publication.publication_id'), nullable=False)

class Professions(db.Model):
    profession_id   = db.Column(db.Integer, primary_key=True)
    profession_name = db.Column(db.String(120), nullable=False)
    professional = db.relationship('Person', secondary=person_profession, back_populates='profession')
    
    def repr(self):
        return f"<User {self.profession_id}>"


