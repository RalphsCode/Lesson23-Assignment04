from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import Register, Login, Feedback_Form
from static.functions import end_session

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
    """App home page, showing links to the various views"""
    return render_template('home.html')

@app.route('/')
def slash():
    """App start page"""
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Shows and Processes form to register a new user"""
    form = Register()
    # using a try/except block in case there is no username variable stored in session
    try:

        if session['username']:
             # if a user is already logged in, log them out;
            end_session()
            if form.validate_on_submit(): # only works on the post request
                flash("Form Submitted Successfully.")
                username = form.username.data
                password = form.password.data
                # Hash the password *** NOT USED ***
                # password_hashed = hash(password)
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

                # Forward the user to their profile page
                return redirect(f"/users/{username}")

        # GET route, to display the new user registration page
        return render_template('register.html', form=form)
    
    # If there is no username session variable
    except KeyError:
        flash("Please log in to access this page")
        return redirect("/login")


@app.route('/login', methods=["GET", "POST"])
def login():
    """User log in page"""
    form = Login()
    # POST route
    if form.validate_on_submit(): # only works on the post request
        username = form.username.data
        password = form.password.data
        # Hash the password  *** NOT USED ***
        # password_hashed = hash(password)

        # Retrieve the entered username from the user table / database
        curr_user = User.query.filter(User.username == username).first()
        # Check if the username that the user eneted was found in the database
        if curr_user:
            # Check if the username's password was entered correctly
            if curr_user.password == password:
                # set the user session variable 
                session['username'] = [username]
                flash(f'Found username "{username}" in database, and password matched.')
                # Forward user to their profile page
                return redirect(f'/users/{username}')
            # If the entered password is incorrect
            else:
                flash(f'Found username "{username}" in database, BUT password ({password} was not correct.')
                return redirect("/login")
            
        # If the username was not found in the database:
        else:
            flash(f'Did NOT find user "{username}" in database.')
            return redirect("/login")
    
    # GET Route - displays the log in form:
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Logs a user out of the app / session"""
    end_session()
    return redirect("/home")


@app.route('/users/<username>')
@app.route('/users/<username>/feedback/add')
def profile(username):
    """Displays the user's profile & feedback posts"""
    # using a try/except block in case there is no username variable stored in session
    try:
        # Check that the user is logged in
        if username in session['username']:
            form = Feedback_Form()
            # Get the user's profile information from the database:
            user = User.query.filter(User.username == username).first()
            # Check if the user has any feedback in the database:
            if Feedback.query.filter(Feedback.username == username).first():
                # Get the user's feedback posts from the database:
                posts = Feedback.query.filter(Feedback.username == username).all()
                # Display the user's profile and feedback:
                return render_template('user_profile.html', user=user, form=form, posts=posts)
            # If no feedback posts; display the user's profile (without posts)
            return render_template('user_profile.html', user=user, form=form)
        # if correct user is not logged in:
        else:
            flash("You must be logged in to see that page")
            return redirect("/login")

    # If there is no username variable in session:    
    except KeyError:
        return redirect("/")
    

@app.route('/users/<username>/delete')
def delete(username):
    """Functionality to DELETE a user and his/her feedback posts """
    # Check if correct user logged in:
    if username in session['username']:
        # Check if the user has any feedback posts in the database:
        if Feedback.query.filter(Feedback.username == username).first():
            # delete the user's posts
            Feedback.query.filter(Feedback.username == username).delete()
        # Delete the user profile from the database
        User.query.filter(User.username == username).delete()
        db.session.commit()
        # Clear the user out of session
        session.pop('username')
        return redirect("/")
    # If a different user is logged in:
    else:
        flash("You do not have access to delete user. Please log in again.")
        end_session()
        return redirect ("/")
    

@app.route('/users/<username>/feedback/add', methods=["POST"])
def add_feedback(username):
    """Functionality for a user to add feedback"""
    form = Feedback_Form()
    # POST route
    if form.validate_on_submit():
        # Get the data from the form
        feedback = form.feedback.data
        # Retrieve the user details from the database
        User.query.filter(User.username == username).first()
        # Create a new_feedback object
        new_feedback = Feedback(title="Feedback", content= feedback, username=username)

        with app.app_context():
            # Add objects to the database
            db.session.add(new_feedback)
            db.session.commit()

    # Send user to their profile page
    return redirect(f"/users/{username}")    

        

