"""Repository for functions used in the app"""

from flask import session


def check_login(username ="no_user"):
    """Returns True if user logged in """
    try: 
        if username in session['username']:
            return True
    except KeyError:
        return False


def end_session():
    """Deletes a user from session / ends a user session"""
    if check_login():
        session.pop('username')
    return True