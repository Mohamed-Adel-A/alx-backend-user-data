#!/usr/bin/env python3
"""
Main Flask app
"""
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """Route handler for the index page"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
