from models import db, User, Feedback
from app import app

# Drop & Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

# Empty table
# User.query.delete()

# Add users
u1 = User(username="BaconLover4Life", password="123", email="bacon.sizzle@nomail.com", first_name="Chris P.", last_name="Bacon")
u2 = User(username="KeyboardWarrior", password="qwe", email="code247e@nomail.com", first_name="Anita", last_name="Bath")
u3 = User(username="CoffeeAddict123", password="zzz", email="buzzed@nomail.com", first_name="Stuart", last_name="Bucks")
u4 = User(username="BackwardThinker", password="321", email="wait_what@nomail.com", first_name="Justin", last_name="Tyme")

with app.app_context():
    # Add objects to the session
    db.session.add_all([u1, u2, u3, u4])
    # Commit to database
    db.session.commit()

# Add feedback
f1 = Feedback(title="My first feedback.", content="This app is totally sick!", username="KeyboardWarrior")
f2 = Feedback(title="Not a fan", content="This app's visually are pathetic!", username="BackwardThinker")
f3 = Feedback(title="Update.", content="I thought this app was totally sick, but now I'm not sure!", username="KeyboardWarrior")
f4 = Feedback(title="Needs work.", content="This app works great, but the visuals are lacking.", username="KeyboardWarrior")

with app.app_context():
    # Add objects to the session
    db.session.add_all([f1, f2, f3, f4])
    # Commit to database
    db.session.commit()