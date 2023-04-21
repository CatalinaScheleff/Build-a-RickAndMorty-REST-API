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
from models import db, User
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route("/personajes", methods=['GET'])
def get_personajes():
    return "lista de personajes"

@app.route("/personajes/<int:personaje_id>", methods=['GET'])
def get_personaje(personaje_id):
    return "lista de personajes[personaje_id]"

@app.route("locations", methods=['GET'])
def get_locations():
    return "lista de locations"

@app.route("locations/<int:location_id>", methods=['GET'])
def get_location(location_id):
    return "lista de locations[location_id]"


@app.route("/users", methods=['GET'])
def get_users():
    return "lista de usuarios"

@app.route("/users/favorites", methods=['GET'])
def get_favorites():
    return "lista de favoritos de un usuario"

@app.route("/favorite/locations/<int:location_id>", methods=['POST'])
def add_location(location_id):
    return "Agregar favorito [location_id]"

@app.route("/favorite/personajes/<int:personaje_id>", methods=['POST'])
def add_location(personaje_id):
    return "Agregar favorito [personaje_id]"

@app.route("/favorite/personajes/<int:personaje_id>", methods=['DELETE'])
def add_location(personaje_id):
    return "Eliminar favorito [personaje_id]"

@app.route("/favorite/locations/<int:location_id>", methods=['DELETE'])
def add_location(location_id):
    return "Eliminar favorito [location_id]"

    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
