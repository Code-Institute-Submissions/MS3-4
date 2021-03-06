"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, jsonify, request, session, url_for, redirect
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo
import pymongo
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
    num_categories =mongo.db.categories.count()
    start = int(uniform(1,num_categories - 8))
    category = mongo.db.categories.find()[start:start+8]

    categories = random_category_recipe(list(category))
    categories2 = []
    current_page = []
    count = 0
    for c in categories:
        current_page.append(c)
        count+=1
        if count % 4 == 0:
            categories2.append(current_page)
            current_page = []

    recipes = []
    chosen_ids = []
    recipe_ids = list(mongo.db.recipes.find({}, projection={'_id': True}))
    count = 0
    current_page = []
    while count < 16:
        
        idx = floor(uniform(0,len(recipe_ids)))
        try:
            exists = chosen_ids.index(idx)
        except:
            recipe = mongo.db.recipes.find_one({"_id": recipe_ids[idx]['_id']})
            chosen_ids.append(idx)
            current_page.append(recipe)
            count+=1
            if count % 4 == 0:
                recipes.append(current_page)
                current_page = []
        
        
    
    return render_template(
        'index.html',
        title='Home Page',
        recipe=recipe,
        recipes=recipes,
        year=datetime.now().year,
        categories=categories2
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
    time = int(time)
    hours = floor(int(time)/3600) 
    takeaway_hours = hours*60 
    minutes = (int(time) / 60) - takeaway_hours
    if hours< 1:
        if int(time)/60 > 1:
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
        new_id = add_recipe(Name, Description, Steps, Ingredients,Categories,TotalTime, recipeImage)
        return redirect(f'/recipe/{new_id}')
    return render_template('addrecipe.html', 
        Name = "",
        TotalTime = "",
        recipeImage = ""
    )

def add_recipe(Name, Description, Steps, Ingredients, Categories, TotalTime, recipeImage):
    recipe_id = get_next_recipe()
    ingredientsList = Ingredients.split('\r\n')
    categoriesList = Categories.split('\r\n')
    stepsList = Steps.split('\r\n')

    for category in categoriesList:
        if (category != ''):
            cat = mongo.db.categories.find_one({'Name': category})
            if cat == None:
                mongo.db.categories.insert_one({'_id': get_next_category(), 'Name': category, 'Recipes': [{'_id': recipe_id, 'Name': Name, 'Description': Description, 'TotalTime': TotalTime, 'Image': recipeImage}]})
            else:
                recs = cat['Recipes']
                recs.append({'_id': recipe_id, 'Name': Name, 'Description': Description, 'TotalTime': TotalTime, 'Image': recipeImage})
                mongo.db.categories.find_one_and_update({'_id': cat['_id']}, {"$set":  {'Recipes': recs}})
    mongo.db.recipes.insert_one({'_id': recipe_id, 'Name': Name, 'Description': Description, 'Steps': stepsList, 'Ingredients': ingredientsList, 'Categories': categoriesList, 'TotalTime': TotalTime, 'Image': recipeImage})
    return recipe_id


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

@app.route('/recipe/<recipe_id>/edit', methods=['GET', 'POST'])
def editrecipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id":int(recipe_id)})
    if request.method == 'POST':
        data = request.form
        Name = data["Name"]
        Description = data["Description"]
        Steps = data["Steps"]
        Ingredients = data["Ingredients"]
        Categories = data["Categories"]
        TotalTime = data["TotalTime"]
        recipeImage = data["recipeImage"]
        new_id = edit_recipe(recipe['_id'], recipe, Name, Description, Steps, Ingredients,Categories,TotalTime, recipeImage)
        return redirect(f'/recipe/{new_id}')


    return render_template('editrecipe.html',
        recipe=recipe,
        ings = "\n".join(recipe['Ingredients']),
        steps = "\n\n".join(recipe['Steps']),
        cats = "\n".join(recipe['Categories'])
    )

def edit_recipe(recipe_id, recipe, Name, Description, Steps, Ingredients, Categories, TotalTime, recipeImage):
    next_cat = get_next_category()
    next_recipe = get_next_recipe()
    ingredientsList = Ingredients.split('\r\n')
    categoriesList = Categories.split('\r\n')
    stepsList = Steps.split('\r\n\r\n')
    


    for category in categoriesList:
        if (category != ''):
            cat = mongo.db.categories.find_one({'Name': category})
            if cat == None:
                mongo.db.categories.insert_one({'_id': get_next_category(), 'Name': category, 'Recipes': [{'_id': recipe_id, 'Name': Name, 'Description': Description, 'TotalTime': TotalTime, 'Image': recipeImage}]})
            else:
                existsInCat = False
                recs = cat['Recipes']
                for rec in recs:
                    if rec['_id'] == recipe_id:
                        existsInCat = True
                
                if not existsInCat: 
                    recs.append({'_id': recipe_id, 'Name': Name, 'Description': Description, 'TotalTime': TotalTime, 'Image': recipeImage})
                    mongo.db.categories.find_one_and_update({'_id': cat['_id']}, {"$set":  {'Recipes': recs}})
    
    for category in recipe['Categories']:
        existsInNewList = False
        for newCategory in categoriesList:
            if newCategory == category:
                existsInNewList = True

        if not existsInNewList:
            cat = mongo.db.categories.find_one({'Name': category})
            recs = []

            for rec in cat['Recipes']:
                if rec['_id'] != recipe_id:
                    recs.append(rec)
            mongo.db.categories.find_one_and_update({'_id': cat['_id']}, {"$set":  {'Recipes': recs}})
            if (len(recs) == 0):
                mongo.db.categories.delete_one({'_id': int(cat['_id'])})
    mongo.db.recipes.find_one_and_update({'_id': recipe_id,}, {"$set": { 'Name': Name, 'Description': Description, 'Steps': stepsList, 'Ingredients': ingredientsList, 'Categories': categoriesList, 'TotalTime': TotalTime, 'Image': recipeImage}})
    return recipe_id
def get_next_category():
    last_doc = mongo.db.categories.find_one({}, sort=[('_id', pymongo.DESCENDING)])
    return int(last_doc['_id']) + 1
def get_next_recipe():
    last_doc = mongo.db.recipes.find_one({}, sort=[('_id', pymongo.DESCENDING)])
    
    return int(last_doc['_id']) + 1