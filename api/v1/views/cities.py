#!/usr/bin/python3
""" cities """


from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def all_cities(state_id):
    """ Return all cities in a state """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """ Return a city """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Delete a city """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Create a city """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    city = request.get_json()
    if city is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in city:
        return jsonify({"error": "Missing name"}), 400
    city["state_id"] = state_id
    new_city = City(**city)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Update a city """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())


@app_views.route('/cities/search', methods=['POST'], strict_slashes=False)
def search_city():
    """ Search for a city """
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    cities = storage.search("City", data["name"])
    return jsonify([city.to_dict() for city in cities])
