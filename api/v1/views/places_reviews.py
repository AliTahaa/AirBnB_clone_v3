#!/usr/bin/python3
""" places_reviews """

from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def all_reviews(place_id):
    """ Return all reviews in a place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """ Return a review """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete a review """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Create a review """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    review = request.get_json()
    if review is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in review:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get("User", review["user_id"])
    if user is None:
        abort(404)
    if "text" not in review:
        return jsonify({"error": "Missing text"}), 400
    review["place_id"] = place_id
    new_review = Review(**review)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Update a review """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
