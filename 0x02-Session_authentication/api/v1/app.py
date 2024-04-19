#!/usr/bin/env python3
"""
Route module for the API
"""
import os
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)

from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.auth.session_exp_auth import SessionExpAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = getenv('AUTH_TYPE', 'auth')


if AUTH_TYPE == 'basic_auth':
    auth = BasicAuth()

if AUTH_TYPE == 'session_auth':
    auth = SessionAuth()

if AUTH_TYPE == 'session_exp_auth':
    auth = SessionExpAuth()

if AUTH_TYPE == 'session_db_auth':
    auth = SessionDBAuth()

if AUTH_TYPE == 'auth':
    auth = Auth()


@app.before_request
def before_request_handler():
    """
    Filter requests using flask before_request method.
    """
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/'
                      ]

    if auth.require_auth(request.path, excluded_paths):
        auth_header = auth.authorization_header(request)
        auth_cookie = auth.session_cookie(request)
        if auth_header is None and auth_cookie is None:
            abort(401)

        request.current_user = auth.current_user(request)
        if request.current_user is None:
            abort(403)


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler
    """
    response = jsonify({"error": "Forbidden"})
    response.status_code = 403
    return response


@app.errorhandler(401)
def not_authorized(error) -> str:
    """ Unauthorized handler
    """
    response = jsonify({"error": "Unauthorized"})
    response.status_code = 401
    return response


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
