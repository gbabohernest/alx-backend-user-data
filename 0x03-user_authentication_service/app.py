#!/usr/bin/env python3
"""Defines a Basic Flask application"""

from flask import Flask, jsonify, request

from auth import Auth

app = Flask(__name__)
AUTH = AUTH()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    Route handler for the root endpoint ("/")

    Returns:
        JSON: A JSON response with a welcome message
    """
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    Route handler for the POST /users endpoint
    to register a new user.

    Returns:
        JSON: A JSON response indicating success or failure
              of user registration.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        # email = request.form.get("email")
        # password = request.form.get("password")

        user = AUTH.register_user(email, password)
        response = {"email": user.email, "message": "user created"}
        return jsonify(response)

    except ValueError:
        response = {"message": "email already registered"}
        return jsonify(response), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
