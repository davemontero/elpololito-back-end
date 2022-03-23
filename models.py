from enum import unique
from tkinter.tix import COLUMN
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()



class User(db.Model):
    user_id   = db.Column(db.Integer, primary_key=True)
    umail = db.Column(db.String(120), unique=True, nullable=False)
    upass   = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'), nullable=False)
    pololito =  db.relationship('Pololito', backref='pololito', lazy=True)

    def __repr__(self):
        return f"<User {self.user_id}>"

    def serialize(self):
        return {
            "mail": self.umail,
            "pass": self.upass
        }

# person_profession = db.Table('person_profession', 
#     db.Column('fk_person_id', db.Integer, db.ForeignKey('person.person_id')), 
#     db.Column('fk_profession_id', db.Integer, db.ForeignKey('professions.profession_id')))
class Person(db.Model):
    person_id     = db.Column(db.Integer, primary_key=True)
    pfname  = db.Column(db.String(50), nullable=False)
    psname  = db.Column(db.String(50))
    plname  = db.Column(db.String(50), nullable=False)
    plname2 = db.Column(db.String(50))
    prut    = db.Column(db.Integer, unique=True, nullable=False)
    pphone  = db.Column(db.Integer)
    pdob    = db.Column(db.Date, nullable=False) 
    pgender = db.Column(db.String(10))
    pphoto  = db.Column(db.String(50))
    # profession = db.relationship("Profession", 
    #                     secondary = person_profession,
    #                     backref="Person")
    # user    = db.relationship('User', backref='person', lazy=True)

    def __repr__(self):
        return f"<Professional {self.person_id}>"
    
    def serialize(self):
        return {
            "person_id": self.person_id,
            "fullname": f"{self.pfname} {self.plname}"
        }


# class Professions(db.Model):
#     profession_id   = db.Column(db.Integer, primary_key=True)
#     profession_name = db.Column(db.String(120), nullable=False)
#     professional = db.relationship('person', secondary=person_profession, backref='profession')
#     def repr(self):
#         return f"<User {self.user_id}>"



class Employer(db.Model):
    employer_id     = db.Column(db.Integer, primary_key=True)
    pfname  = db.Column(db.String(50), nullable=False)
    psname  = db.Column(db.String(50))
    plname  = db.Column(db.String(50), nullable=False)
    plname2 = db.Column(db.String(50))
    prut    = db.Column(db.Integer, unique=True, nullable=False)
    pphone  = db.Column(db.Integer)
    pdob    = db.Column(db.Date, nullable=False) 
    pgender = db.Column(db.String(10))
    paddress = db.Column(db.String(50))
    paddress2 = db.Column(db.String(50))
    pcity = db.Column(db.String(50))
    
    def __repr__(self):
        return f"<Employer {self.employer_id}>"
    
    def serialize(self):
        return {
            "employer_id": self.employer_id,
            "fullname": f"{self.pfname} {self.plname}"
        }

  
class Publication(db.Model):
    publication_id      = db.Column(db.Integer, primary_key=True)
    publication_desc    = db.Column(db.Text(1000), nullable=False)
    publication_place   = db.Column(db.String(50), nullable=True)
    create_at           = db.Column(db.DateTime, default=datetime.now())
    fk_user_id          = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def repr(self):
        return f"<Publication {self.publication_id}>"

class Pololito(db.Model):
    pololito_id = db.Column(db.Integer, primary_key=True)
    pololito_rating  = db.Column(db.Enum('1','2','3','4','5'), nullable=True)
    pololito_status  = db.Column(db.Boolean, default=True, unique=False)
    create_at        = db.Column(db.DateTime, default=datetime.now())
    fk_user_id       = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)