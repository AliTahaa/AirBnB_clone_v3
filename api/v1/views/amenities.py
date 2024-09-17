#!/usr/bin/python3
""" amenities """

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/amenities', strict_slashes=False)
def all_amenities():
    """ Return all amenities """
    return jsonify(
        [amenity.to_dict() for amenity in storage.all("Amenity").values()])


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """ Return an amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Delete an amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Create an amenity """
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    amenity = request.get_json()
    if amenity is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in amenity:
        return jsonify({"error": "Missing name"}), 400
    new_amenity = Amenity(**amenity)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Update an amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
