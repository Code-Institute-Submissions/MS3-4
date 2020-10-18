"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, jsonify
from MS3_Cookbook import app
from flaskext.mysql import MySQL


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'cookbook'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)




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
        message='Your application description page.'
    )

@app.route('/api/auth')
def auth():
    conn = mysql.connect()
    cursor =conn.cursor()

    cursor.execute("SELECT * from recipe")
    data = cursor.fetchone()
 
    password = "hello"
    return jsonify(password=password)