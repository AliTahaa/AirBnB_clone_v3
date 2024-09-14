#!/usr/bin/python3
""" Flask app """

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """ 404 """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(exception):
    """teardown"""
    storage.close()


if __name__ == "__main__":
    HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = getenv("HBNB_API_PORT", 5000)
    app.run(host=HOST, port=PORT, threaded=True)
