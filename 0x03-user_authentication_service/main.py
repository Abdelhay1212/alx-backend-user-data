#!/usr/bin/env python3
"""End-to-end integration test
"""
import requests

URL = 'http://localhost:5000/'

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """test registering a user
    """
    data = {'email': email, 'password': password}

    response = requests.post(URL+'/users', data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

    response = requests.post(URL+'/users', data=data)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """test log in a user with wrong credentials
    """
    data = {'email': email, 'password': password}

    response = requests.post(URL+'/sessions', data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """test log in a user
    """
    data = {'email': email, 'password': password}

    response = requests.post(URL+'/sessions', data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """test profile unlogged
    """
    response = requests.get(URL+'/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """test profile logged
    """
    cookies = {'session_id': session_id}
    response = requests.get(URL+'/profile', cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """test log out a user
    """
    response = requests.delete(URL+'/sessions')
    assert response.status_code == 403

    cookies = {'session_id': 'wrongsessionid'}
    response = requests.delete(URL+'/sessions', cookies=cookies)
    assert response.status_code == 403

    cookies = {'session_id': session_id}
    response = requests.delete(URL+'/sessions', cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """test resetting a password token
    """
    data = {'email': email}

    response = requests.post(URL+'/reset_password', data=data)
    assert response.status_code == 200
    assert 'email' in response.json()
    assert response.json().get('email') == email
    assert 'reset_token' in response.json()
    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """test updating a user password
    """
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }

    response = requests.put(URL+'/reset_password', data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


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
