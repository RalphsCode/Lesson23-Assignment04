"""Repository for functions used in the app"""

from flask import session

def end_session():
    """Deletes a user from session / ends a user session"""
    session.pop('username')
    return True

