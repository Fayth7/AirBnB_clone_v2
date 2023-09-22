#!/usr/bin/python3
"""Starts a Flask web application."""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_db(error):
    """Closes the database after each request."""
    storage.close()


@app.route('/cities_by_states')
def cities_by_states():
    """Display a list of states and their cities."""
    states = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
