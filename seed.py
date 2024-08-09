from models import db, User
from app import app

# Drop & Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

# Empty table
# User.query.delete()

# Add users
u1 = User(username="BaconLover4Life", password="baconBaconbaCon", email="bacon.sizzle@nomail.com", first_name="Chris P.", last_name="Bacon")
u2 = User(username="KeyboardWarrior", password="qwerty", email="code247e@nomail.com", first_name="Anita", last_name="Bath")
u3 = User(username="CoffeeAddict123", password="DailyGrind007", email="buzzed@nomail.com", first_name="Stuart", last_name="Bucks")
u4 = User(username="BackwardThinker", password="EinsteinWasAllWrong1959", email="wait_what@nomail.com", first_name="Justin", last_name="Tyme")

with app.app_context():
    # Add objects to the session
    db.session.add_all([u1, u2, u3, u4])
    # Commit to database
    db.session.commit()