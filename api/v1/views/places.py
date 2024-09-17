#!/usr/bin/python3
""" places """

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """ Return all places in a city """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """ Return a place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Delete a place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Create a place """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    place = request.get_json()
    if place is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in place:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get("User", place["user_id"])
    if user is None:
        abort(404)
    if "name" not in place:
        return jsonify({"error": "Missing name"}), 400
    place["city_id"] = city_id
    new_place = Place(**place)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Update a place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_place():
    """ Search for a place """
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    places = []
    if data:
        states = data.get("states")
        cities = data.get("cities")
        amenities = data.get("amenities")
        if not states and not cities and not amenities:
            return jsonify({"error": "Missing states or cities or amenities"}),
        400
        if states:
            for state_id in states:
                state = storage.get("State", state_id)
                if state:
                    for city in state.cities:
                        for place in city.places:
                            places.append(place)
        if cities:
            for city_id in cities:
                city = storage.get("City", city_id)
                if city:
                    for place in city.places:
                        places.append(place)
        if amenities:
            for amenity_id in amenities:
                amenity = storage.get("Amenity", amenity_id)
                if amenity:
                    for place in amenity.places:
                        places.append(place)
    else:
        places = storage.all("Place").values()
    return jsonify([place.to_dict() for place in places])
