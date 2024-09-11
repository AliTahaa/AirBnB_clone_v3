#!/usr/bin/python3
"""
Blueprint for API
"""

from api.v1.views import app_views
from flask import Flask, jsonify

app = Flask(__name__)


@app_views.route('/status')
def api_status():
    """ Return status """
    response = {"status": "OK"}
    return jsonify(response)

@app_views.route('/stats')
def api_stats():
    """ Return stats """
    from models import storage
    classes = {"Amenity": "amenities", "City": "cities", "Place": "places",
               "Review": "reviews", "State": "states", "User": "users"}
    response = {}
    for key, value in classes.items():
        response[value] = storage.count(key)
    return jsonify(response)
