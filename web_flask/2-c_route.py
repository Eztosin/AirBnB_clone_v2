#!/usr/bin/python3
"""contains a script that starts a Flask web application"""
from flask import Flask


app = Flask("__name__")


@app.route('/', strict_slashes=False)
def hello():
    """displays a message"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """displays a message"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def display_c(text):
    """displays “C” followed by the value of the text variable"""
    return "C {}".format(text.replace('_', ' '))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
