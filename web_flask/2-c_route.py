#!/usr/bin/python3
"""
Starts a Flask web application.
"""

from flask import Flask, escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Defines a route that displays "Hello HBNB!"
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Defines a route that displays "HBNB"
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """
    Defines a route that displays "C " 
    followed by the value of the text variable
    (replace underscore _ symbols with a space)
    """
    return "C {}".format(escape(text).replace('_', ' '))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
