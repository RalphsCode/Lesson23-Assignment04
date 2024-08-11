from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# models

class User(db.Model):
    """User table to track users and their password hash"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key= True)
    
    password = db.Column(db.Text,
                     nullable=False)

    email = db.Column(db.String(50), nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    
class Feedback(db.Model):
    """Stores the user's feedback"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.String, nullable=False)

    username = db.Column(db.String, db.ForeignKey('users.username'))
