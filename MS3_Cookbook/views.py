"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, jsonify
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo
from MS3_Cookbook import app



mongo = PyMongo(app)



@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.')

@app.route('/api/auth')
def auth():
    online_users = mongo.db.cookbook.find({})
    #x = online_users.count_documents;
    return jsonify(password=online_users)
 





### mongo "mongodb+srv://cookbook.3ljpp.mongodb.net/Cookbook" --username Lou