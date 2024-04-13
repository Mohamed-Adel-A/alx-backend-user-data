#!/usr/bin/python3
"""
main.py
"""
from flask import jsonify, request, abort, make_response
from auth import Auth
from app import app

AUTH = Auth()


@app.route('/register', methods=['POST'])
def register():
    """
    Register route
    """
    if not request.json or 'email' not in request.json or 'password' not in request.json:
        abort(400)
    try:
        email = request.json['email']
        password = request.json['password']
        user = AUTH.register_user(email, password)
        return jsonify({'message': f"User {user.email} successfully registered"}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    """
    Login route
    """
    if not request.json or 'email' not in request.json or 'password' not in request.json:
        abort(400)
    email = request.json['email']
    password = request.json['password']
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    if not session_id:
        abort(500)
    return jsonify({'session_id': session_id}), 200

@app.route('/logout', methods=['POST'])
def logout():
    """
    Logout route
    """
    if not request.json or 'session_id' not in request.json:
        abort(400)
    session_id = request.json['session_id']
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(401)
    AUTH.destroy_session(user.id)
    return jsonify({'message': 'Logout successful'}), 200

@app.errorhandler(400)
def bad_request(error):
    """
    Error handler for bad requests
    """
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(401)
def unauthorized(error):
    """
    Error handler for unauthorized access
    """
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(500)
def internal_server_error(error):
    """
    Error handler for internal server errors
    """
    return make_response(jsonify({'error': 'Internal server error'}), 500)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
