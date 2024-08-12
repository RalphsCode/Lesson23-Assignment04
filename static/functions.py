"""Repository for functions used in the app"""

from flask import session

def end_session():
    """Deletes a user from session / ends a user session"""
    session.pop('username')
    return True

def check_login(username):
    """Returns True if user logged in """
    if username in session['username']:
        return True
    return False