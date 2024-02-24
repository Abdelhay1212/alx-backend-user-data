#!/usr/bin/env python3
"""Basic Flask app
"""
from auth import Auth
from flask import Flask, request, jsonify, abort, redirect


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
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify(
            {
                "email": email,
                "message": "user created"
            }
        )
    except ValueError:
        return jsonify({"message": "email already registered"})


@app.route('/sessions', methods=['POST', 'DELETE'], strict_slashes=False)
def handle_sessions():
    """log in a user
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if AUTH.valid_login(email=email, password=password):
            session_id = AUTH.create_session(email=email)
            resp = jsonify({"email": email, "message": "logged in"})
            resp.set_cookie("session_id", session_id)
            return resp
        abort(401)

    if request.method == 'DELETE':
        session_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id)
        if user is not None:
            AUTH.destroy_session(user.id)
            return redirect('/')
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
