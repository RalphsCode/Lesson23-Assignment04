from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
# from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Feedback
from forms import Register, Login, Feedback_Form

# app configuration files
app = Flask(__name__)
app.config['SECRET_KEY'] = "RalphsCode123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ponderosa@localhost/flask_feedback'
app.config['SECRET_KEY'] = 'RalphsCode123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    db.create_all()

@app.route('/home')
def home():
    """App home page"""
    return render_template('home.html')

@app.route('/')
def slash():
    """App start page"""
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Shows and Processes form to register a new user"""
    form = Register()
    if form.validate_on_submit(): # only works on the post request
        flash("Form Submitted Successfully.")
        username = form.username.data
        password = form.password.data
        # Hash the password *** NOT USED ***
        password_hashed = hash(password)
        # password_utf = password_hashed.encode('utf-8')
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # create a new_user object
        new_user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        # insert the new_user object into the database
        db.session.add(new_user)
        db.session.commit()

        # set the user session variable 
        session['username'] = [username]
        return redirect('/secret')

    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = Login()
    if form.validate_on_submit(): # only works on the post request
        username = form.username.data
        password = form.password.data
        # Hash the password  *** NOT USED ***
        password_hashed = hash(password)
        curr_user = User.query.filter(User.username == username).first()
        if curr_user:
            if curr_user.password == password:
                # set the user session variable 
                session['username'] = [username]
                flash(f'Found username "{username}" in database, and password matched.')
                return redirect(f'/users/{username}')
            else:
                flash(f'Found username "{username}" in database, BUT password ({password} was not correct.')
                return redirect("/login")
        else:
            flash(f'Did NOT find user "{username}" in database.')
            return redirect("/login")

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect("/home")

@app.route('/users/<username>')
def profile(username):
    if username in session['username']:
        form = Feedback_Form()
        user = User.query.filter(User.username == username).first()
        if Feedback.query.filter(Feedback.username == username).first():
            posts = Feedback.query.filter(Feedback.username == username).all()
            return render_template('user_profile.html', user=user, posts=posts, form=form)
        else:
            flash("You may not access the profile, nor modify the feedback, of others")
            return render_template('user_profile.html', user=user)
    else:
        flash("You must be logged in to see that page")
        return redirect("/login")
    
@app.route('/users/<username>/delete')
def delete(username):
    if username in session['username']:
        if Feedback.query.filter(Feedback.username == username).first():
            Feedback.query.filter(Feedback.username == username).delete()
        User.query.filter(User.username == username).delete()
        db.session.commit()
        session.pop('username')
        return redirect("/")
    else:
        flash("You do not have access to delete user. Please log in again.")
        session.pop('username')
        return redirect ("/")
    
@app.route('/users/<username>/feedback/add', methods=["POST"])
def add_feedback(username):
    form = Feedback_Form()
    # POST route
    if form.validate_on_submit():
        feedback = form.feedback.data
        User.query.filter(User.username == username).first()
        new_feedback = Feedback(title="Feedback", content= feedback, username=username)

        with app.app_context():
            # Add objects to the session
            db.session.add(new_feedback)
            # Commit to database
            db.session.commit()

    return redirect(f"/users/{username}")    

        

