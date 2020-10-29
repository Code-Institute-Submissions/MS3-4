"""
This script runs the MS3_Cookbook application using a development server.
"""

from os import environ
from MS3_Cookbook import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run('0.0.0.0', PORT, debug=true)
