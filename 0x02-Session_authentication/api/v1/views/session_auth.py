#!/usr/bin/env python3
""" A new flask view that handles all
   routes for the Session Authentication
"""
from flask import request, jsonify, make_response
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth
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

    session_id = auth.create_session(user.id)

    response_data = user.to_json()
    response = make_response(jsonify(response_data))
    session_name = getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response
