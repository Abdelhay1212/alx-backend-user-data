#!/usr/bin/env python3
""" New view for Session Authentication """
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """login route
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users[0]:
        return jsonify({"error": "no user found for this email"}), 404
    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(users[0].id)
    out = jsonify(users[0].to_json())
    out.set_cookie(session_id, users[0].id)
    return out
