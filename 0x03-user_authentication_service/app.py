#!/usr/bin/env python3
"""
Main Flask app
"""
from flask import Flask, jsonify, request, abort
from flask import make_response, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """Route handler for the index page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """Route handler to register a new user"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """Login route"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(400)

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response, 200
        else:
            abort(500)
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Logout route"""
    session_id = request.cookies.get("session_id")

    if not session_id:
        return make_response(jsonify({"error": "Session ID not found"}), 403)

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        return make_response(jsonify({"error": "User not found"}), 403)


@app.route("/profile", methods=["GET"])
def profile():
    """Profile route"""
    session_id = request.cookies.get("session_id")

    if not session_id:
        return make_response(jsonify({"error": "Session ID not found"}), 403)

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        return make_response(jsonify({"error": "User not found"}), 403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
