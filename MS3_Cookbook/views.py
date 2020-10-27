"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, jsonify
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo
from MS3_Cookbook import app
from random import uniform

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

    recipe1 = mongo.db.recipe.find_one({"_id":1})
    recipe = mongo.db.recipe.find_one({"_id": 26})
    
    recipes1 = mongo.db.recipe.find()[1:5]
    recipes2 = mongo.db.recipe.find()[11:15]
    recipes3 = mongo.db.recipe.find()[21:25]

    return render_template(
        'index.html',
        title='Home Page',
        recipe=recipe,
        recipes=[list(recipes1), list(recipes2), list(recipes3)],
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

@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    recipe = mongo.db.recipe.find_one({"_id":int(recipe_id)})
    
    return render_template(
        'recipe.html',
        title=recipe['Name'],
        recipe=recipe)

@app.route('/recipe/random')
def random_recipe():
    Doc_total = mongo.db.recipe.count()
    random = uniform(1, Doc_total)
    recipe = mongo.db.recipe.find_one({"_id":int(random)})
    
    return render_template(
        'recipe.html',
        title=recipe['Name'],
        recipe=recipe)


@app.route('/api/recipe/<recipe_id>/categories')
def recipe_categories(recipe_id):
    recipe = mongo.db.recipe.find_one({"_id":int(recipe_id)}, projection={"Categories": True})
    
    return jsonify(recipe)


@app.route('/auth/login')
def login_page():
    return render_template(
        'login.html',
        title='Login/Signup'
    )

### mongo "mongodb+srv://cookbook.3ljpp.mongodb.net/Cookbook" --username Lou