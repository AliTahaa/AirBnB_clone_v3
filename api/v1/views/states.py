#!/usr/bin/python3
""" States """

from models import storage
from api.v1.views import app_views
from flask import jsonify, request
from models.state import State


@app_views.route('/states', strict_slashes=False)
def all_states():
    """ Return all states """
    states = storage.all("State")
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>')
def get_state(state_id):
    """ Return a state """
    state = storage.get("State", state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Delete a state """
    state = storage.get("State", state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    try:
        # Delete related cities first
        for city in state.cities:
            storage.delete(city)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Create a state """
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    state = request.get_json()
    if state is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in state:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**state)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Update a state """
    state = storage.get("State", state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
