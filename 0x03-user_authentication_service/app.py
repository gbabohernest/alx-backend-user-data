#!/usr/bin/env python3
"""Defines a Basic Flask application"""

from flask import Flask, jsonify


app = Flask(__name__)

@app.route("/", methods=["GET"])
def index() -> str:
    """
    Route handler for the root endpoint ("/")
    Returns:
        JSON: A JSON response with a welcome message
    """
    message = {"message": "Bienvenue"}
    return jsonify(message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
