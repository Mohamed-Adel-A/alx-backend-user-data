#!/usr/bin/env python3
""" Index view module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request

@app_views.route('/status', methods=['GET'])
def status() -> str:
    """ Returns a JSON """
    return jsonify({"status": "OK"})

@app_views.route('/unauthorized', methods=['GET'])
def unauthorized() -> str:
    """ Returns 401 """
    abort(401)

@app_views.route('/forbidden', methods=['GET'])
def forbidden() -> str:
    """ Returns 403 """
    abort(403)
