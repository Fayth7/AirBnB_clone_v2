#!/usr/bin/python3
"""
Starts a Flask web application.
"""

from flask import Flask, escape, render_template

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
    Defines a route that displays "C " followed by the value of the text variable
    (replace underscore _ symbols with a space)
    """
    return "C {}".format(escape(text).replace('_', ' '))


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text):
    """
    Defines a route that displays "Python " 
    followed by the value of the text variable
    (replace underscore _ symbols with a space)
    Default value for text is "is cool".
    """
    return "Python {}".format(escape(text).replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """
    Defines a route that displays "n is a number" only if n is an integer.
    """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    Defines a route that displays an HTML page only if n is an integer.
    """
    return render_template('6-number_template.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """
    Defines a route that displays an HTML page only if n is an integer.
    """
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
