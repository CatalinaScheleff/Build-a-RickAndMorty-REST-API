from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Personaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return '<Personaje %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return '<Location %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    

class Personaje_fav(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    personaje_id = db.Column(db.Integer, db.ForeignKey('personaje.id'))
    rel_user = db.relationship("User")
    rel_personaje = db.relationship("Personaje")

    def __repr__(self):
        return '<Personaje_fav %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "personaje_id": self.personaje_id,
        }


class Location_fav(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    rel_user = db.relationship("User")
    rel_personaje = db.relationship("Location")

    def __repr__(self):
        return '<Location_fav %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "location_id": self.location_id,
        }
