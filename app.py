from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension


# app configuration files
app = Flask(__name__)
app.config['SECRET_KEY'] = "RalphsCode123"

debug = DebugToolbarExtension(app)

@app.route('/')
def home():
    """App home page"""
    return render_template('home.html')