"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, jsonify, request, session, url_for, redirect
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo
from MS3_Cookbook import app
from random import uniform
from math import floor
import bcrypt 


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

    recipe1 = mongo.db.recipes.find_one({"_id":1})
    recipe = mongo.db.recipes.find_one({"_id": 26})
    
    recipes1 = mongo.db.recipes.find()[1:5]
    recipes2 = mongo.db.recipes.find()[11:15]
    recipes3 = mongo.db.recipes.find()[21:25]

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

@app.route('/categories')
def categories():
    """Renders the categories page."""
    cat_length = mongo.db.categories.count()
    category = mongo.db.categories.find()[1:cat_length]

    categories = random_category_recipe(list(category))
    return render_template(
        'categories.html',
        title='categories',
        year=datetime.now().year,
        categories=categories,
        message='Categories page.')


@app.route('/category/<category_id>')
def category(category_id):
    category = mongo.db.categories.find_one({"_id":int(category_id)})
    
    return render_template(
        'category.html',
        title=category['Name'],
        category=category)

@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id":int(recipe_id)})
    
    return render_template(
        'recipe.html',
        title=recipe['Name'],
        recipe=recipe,
        time=secs_to_hours(recipe['TotalTime'])
    )

@app.route('/recipe/random')
def random_recipe():
    Doc_total = mongo.db.recipes.count()
    random = uniform(1, Doc_total)
    recipe = mongo.db.recipes.find_one({"_id":int(random)})
    
    return render_template(
        'recipe.html',
        title=recipe['Name'],
        recipe=recipe,
        time=secs_to_hours(recipe['TotalTime'])
    )


@app.route('/api/recipe/<recipe_id>/categories')
def recipe_categories(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id":int(recipe_id)}, projection={"Categories": True})
    
    return jsonify(recipe)


@app.route('/auth/login', methods=['GET', 'POST'])
def login_page():
    
    if request.method == 'POST':
        data = request.form
        errors = []
        valid = True
        username = data['username']
        
        password = data['password']
        action = data['action']
        if action == 'register':
            cfmEmail = data['cfmEmail']
            cfmPassword = data['cfmPassword']
            email = data['email']


            if cfmEmail != email: 
                valid = False
                errors.append('Email addresses must match')
            if cfmPassword != password: 
                valid = False
                errors.append('Passwords must match')

            if (valid):
                user = register_user(username, email, password)
            return render_template(
                'login.html',
                title='Login/Signup',
                args=request.args,
                data = data,
                username=username,
                email=email,
                cfmEmail=cfmEmail,
                errors=errors
            )
        if action == 'login':
            logged_in = login_user(username, password)
            if logged_in:
                session['current_user'] = username
                return redirect(url_for('home'))
            return render_template(
                'login.html',
                title='Login/Signup',
                args=request.args,
                data = data,
                username=username,
                errors=errors
            )
        return render_template(
            'login.html',
            title='Login/Signup',
            args=request.args,
            data = data,
            username=username,
            email=email,
            cfmEmail=cfmEmail,
            errors=errors
        )
    return render_template(
            'login.html',
            title='Login/Signup'
        )



def secs_to_hours(time): 
    hours = floor(time/3600) 
    takeaway_hours = hours*60 
    minutes = (time / 60) - takeaway_hours
    if hours< 1:
        if time/60 > 1:
            return str(int(time/60)) + " minutes"
        else:
            return str(int(time/60)) + " minute"
    else:
        if hours == 1:
            return str(int(hours)) + " hour, " + str(int(minutes)) + " minutes"
        return str(int(hours)) + " hours, " + str(int(minutes)) + " minutes"


### mongo "mongodb+srv://cookbook.3ljpp.mongodb.net/Cookbook" --username Lou

def random_category_recipe(categories):
    for cat in categories:
        catRecTotal = len(cat['Recipes'])
        cat['Image'] = cat['Recipes'][floor(uniform(0, catRecTotal))]['Image']
        cat['Recipes'] = []
    return categories

@app.route('/search')
def search():
    searchTerm = request.args['search']
    searchCursor = mongo.db.recipes.find({ "$or": [
        genSearch('Name', searchTerm),
        genSearch('Ingredients', searchTerm),
        genSearch('Description', searchTerm)
    ]})
    searchResults = list(searchCursor)
    
    return render_template(
        'results.html',
        results=searchResults)


def genSearch(name, value):
    return {name:{'$regex': value, "$options" :'i'}}

def register_user(username, email, password):
    hashpw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
    return mongo.db.authors.insert_one({ "username": username, "email": email, "password": hashpw })
def login_user(username, password):
    user = mongo.db.authors.find_one({"username": username})
    # this needs to be encrypted
    if bcrypt.checkpw(password.encode('utf-8'), user['password']): 
        return True
    return False

# code used from: https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions as it's exactly as required for my functionality to log out
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('current_user', None)
    return redirect(url_for('home'))
    
# end of code pasted

@app.route('/recipe/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form
        
        Name = data["Name"]
        Description = data["Description"]
        Steps = data["Steps"]
        Ingredients = data["Ingredients"]
        Categories = data["Categories"]
        TotalTime = data["TotalTime"]
        recipeImage = data["recipeImage"]
        add_recipe(Name, Description, Steps, Ingredients,Categories,TotalTime, recipeImage)
        
    return render_template('addrecipe.html')

def add_recipe(Name, Description, Steps, Ingredients, Categories, TotalTime, recipeImage):
    recipe_id = mongo.db.recipes.count() + 1
    ingredientsList = Ingredients.split('\r\n')
    categoriesList = Categories.split('\r\n')
    stepsList = Steps.split('\r\n')
    
    return mongo.db.recipes.insert_one({'_id': recipe_id, 'Name': Name, 'Description': Description, 'Steps': stepsList, 'Ingredients': ingredientsList, 'Categories': categoriesList, 'TotalTime': TotalTime, 'Image': recipeImage})

@app.route('/recipe/<recipe_id>/delete', methods=['GET'])
def delete(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id":int(recipe_id)})

    for cat in recipe['Categories']:
        recs = []
        category = mongo.db.categories.find_one({'Name': cat})
        for recipe in category['Recipes']:
            if recipe['_id']  != int(recipe_id):
                recs.append(recipe)
        mongo.db.categories.find_one_and_update({"_id": int(category['_id'])}, {"$set": {"Recipes": recs}})   
        if (len(recs) == 0):
            mongo.db.categories.delete_one({'_id': int(category['_id'])})
    mongo.db.recipes.delete_one({'_id': int(recipe_id)})
    return redirect(url_for('home'))  

