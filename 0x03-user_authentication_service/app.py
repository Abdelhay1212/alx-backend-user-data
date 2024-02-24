#!/usr/bin/env python3
"""Basic Flask app
"""
from auth import Auth
from flask import Flask, request, jsonify, abort


AUTH = Auth()
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def root():
    """root route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """register a user if doesn't exist
    """
    email = request.get_data("email")
    password = request.get_data("password")

    try:
        AUTH.register_user(email, password)
        return jsonify(
            {
                "email": "<registered email>",
                "message": "user created"
            }
        )
    except ValueError:
        return jsonify({"message": "email already registered"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """log in a user
    """
    email = request.get_data('email')
    password = request.get_data('password')

    if AUTH.valid_login(email=email, password=password):
        session_id = AUTH.create_session(email=email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", session_id)
        return resp
    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
