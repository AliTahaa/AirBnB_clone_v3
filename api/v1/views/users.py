#!/usr/bin/python3
""" users """

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/users', strict_slashes=False)
def all_users():
    """ Return all users """
    return jsonify([user.to_dict() for user in storage.all("User").values()])


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """ Return a user """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Delete a user """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Create a user """
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    user = request.get_json()
    if user is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in user:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in user:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**user)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Update a user """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
