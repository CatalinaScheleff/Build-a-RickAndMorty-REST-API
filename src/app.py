"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personaje, Location, Personaje_fav, Location_fav
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# Get a list of all the characters in the database
@app.route("/personajes", methods=['GET'])
def get_personajes():
    all_characters = Personaje.query.all()
    # result= []
    # for character in all_characters:
    # result.append(character.serialize())
    result = list(map(lambda character: character.serialize(), all_characters))
    print(all_characters)
    return jsonify(result)

# Get a one single character information
@app.route("/personajes/<int:personaje_id>", methods=['GET'])
def get_personaje(personaje_id):
    one_character = Personaje.query.get(personaje_id)
    if (one_character is None):
        return jsonify({"mensaje": "no existe"}),404
    else:
        return jsonify(one_character.serialize())

# Get a list of all the locations in the database
@app.route("/locations", methods=['GET'])
def get_locations():
    all_locations =  Location.query.all()
    result = list(map(lambda location: location.serialize(), all_locations))
    return jsonify(result)

# Get one single location information
@app.route("/locations/<int:location_id>", methods=['GET'])
def get_location(location_id):
    one_location = Location.query.get(location_id)
    if (one_location is None):
        return jsonify({"mensaje":"no existe"}),404
    else:
        return jsonify(one_location.serialize())

# Get a list of all the blog post users
@app.route("/users", methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = list(map(lambda user: user.serialize(), all_users))
    return jsonify(result)



# Get all the favorites that belong to the current user
@app.route("/users/<int:user_id>/favorites", methods=['GET'])
def get_favorites(user_id):
    one_user = User.query.get(user_id)

    personajes_fav = Personaje_fav.query.filter_by(user_id=user_id).all()
    per_fav_serialized = list(map(lambda favorite: favorite.serialize(),personajes_fav))
    
    locations_fav = Location_fav.query.filter_by(user_id=user_id).all()
    loc_fav_serialized = list(map(lambda favorite: favorite.serialize(),locations_fav))

    return jsonify({
        "user_id" : one_user.id,
        "character_favorites": per_fav_serialized,
        "location_favorites": loc_fav_serialized,
    })
    
# Add a new favorite location to the current user with the location id = location_id.
@app.route("/users/<int:user_id>/favorites/location/<int:location_id>", methods=['POST'])
def add_location(user_id, location_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    location = Location.query.get(location_id)
    if location is None:
        return jsonify({"mensaje": "Location no encontrado"}), 404
    
    existing_favorite = Location_fav.query.filter_by(user_id=user_id, location_id=location_id).first()
    if existing_favorite is not None:
        return jsonify({"mensaje": "La ubicación ya está en favoritos"}), 404
    
    new_location_fav = Location_fav(location_id=location_id, user_id=user_id)
    db.session.add(new_location_fav)
    db.session.commit()

    return jsonify(new_location_fav.serialize())

# Add new favorite people to the current user with the character id = personaje_id.
@app.route("/users/<int:user_id>/favorites/personaje/<int:personaje_id>", methods=['POST'])
def add_personaje(user_id, personaje_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    personaje = Personaje.query.get(personaje_id)
    if personaje is None:
        return jsonify({"mensaje": "Personaje no encontrado"}), 404
    
    existing_favorite = Personaje_fav.query.filter_by(user_id=user_id, personaje_id=personaje_id).first()
    if existing_favorite is not None:
        return jsonify({"mensaje": "Personaje ya está en favoritos"}), 404
    
    new_personaje_fav = Personaje_fav(personaje_id=personaje_id, user_id=user_id)
    db.session.add(new_personaje_fav)
    db.session.commit()

    return jsonify(new_personaje_fav.serialize())

# Delete favorite character with the id = personaje_id.
@app.route("/favorites/personajes/<int:personaje_id>", methods=['DELETE'])
def delete_personaje(personaje_id):
    return "Eliminar favorito [personaje_id]"

# Delete favorite location with the id = location_id.
@app.route("/favorites/locations/<int:location_id>", methods=['DELETE'])
def delete_location(location_id):
    return "Eliminar favorito [location_id]"

    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
