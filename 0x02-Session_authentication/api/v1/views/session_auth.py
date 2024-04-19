#!/usr/bin/env python3
""" A new flask view that handles all
   routes for the Session Authentication
"""
from flask import request, jsonify, make_response, abort
from api.v1.views import app_views
from models.user import User
# from api.v1.app import auth
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /api/v1/auth_session/login/
    Return:
        - JSON representation of a User object.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # check if email or password is missing
    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve User instance based on email
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # check if password is valid
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    else:

        from api.v1.app import auth

        session_id = auth.create_session(user.id)

        response_data = user.to_json()
        response = make_response(jsonify(response_data))
        session_name = getenv('SESSION_NAME', '_my_session_id')
        response.set_cookie(session_name, session_id)

        return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    Logout endpoint to delete the user session.

    Returns: An empty JSON response with status code 200 on successful logout,
        or aborts with status code 404 if the session cannot be destroyed.
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
