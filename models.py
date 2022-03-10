from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    pid     = db.Column(db.Integer, primary_key=True)
    pfname  = db.Column(db.String(50), nullable=False)
    psname  = db.Column(db.String(50))
    plname  = db.Column(db.String(50), nullable=False)
    plname2 = db.Column(db.String(50))
    prut    = db.Column(db.Integer, nullable=False)
    pphone  = db.Column(db.Integer)
    pdob    = db.Column(db.Date, nullable=False) 
    pgender = db.Column(db.String(10))
    pphoto  = db.Column(db.String(50))
    user    = db.relationship('User', backref='person', lazy=True)

    def __repr__(self):
        return f"<Person {self.pid}>"
    
    def serialize(self):
        return {
            "pfname":self.pfname,
            "psname":self.psname,
            "plname":self.plname,
            "plname2":self.plname2,
            "prut":self.prut,
            "pphone":self.pphone,
            "pdob":self.pdob,
            "pgender":self.pgender,
            "pphoto":self.pphoto
        }    


class User(db.Model):
    uid   = db.Column(db.Integer, primary_key=True)
    umail = db.Column(db.String(120), unique=True, nullable=False)
    upass = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.pid'), nullable=False)

    def __repr__(self):
        return f"<User {self.uid}>"

    def serialize(self):
        return {
            "mail": self.umail,
            "pass": self.upass
        }