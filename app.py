from flask import Flask, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User
from forms import Register

# app configuration files
app = Flask(__name__)
app.config['SECRET_KEY'] = "RalphsCode123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ponderosa@localhost/flask_feedback'

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
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/home')

    return render_template('register.html', form=form)