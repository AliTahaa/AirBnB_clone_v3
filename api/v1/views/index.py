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
