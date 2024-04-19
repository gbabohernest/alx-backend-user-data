#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
# from views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = getenv('AUTH_TYPE')

if AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth

    auth = BasicAuth()

else:
    from api.v1.auth.auth import Auth as AuthType

    auth = AuthType()


@app.before_request
def before_request_handler():
    """
    Filter requests using flask before_request method.
    """
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']

    if auth.require_auth(request.path, excluded_paths):
        auth_header = auth.authorization_header(request)
        if auth_header is None:
            abort(401)

        request.current_user = auth.current_user(request)
        if request.current_user is None:
            abort(403)
