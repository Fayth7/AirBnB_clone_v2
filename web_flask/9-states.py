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


@app.route('/states')
def states_list():
    """Display a list of states."""
    states = storage.all(State).values()
    return render_template('9-states.html', states=states)


@app.route('/states/<string:id>')
def state_cities(id):
    """Display a list of cities for a specific state."""
    state = storage.get(State, id)
    if state:
        return render_template('9-states.html', state=state)
    return render_template('9-states.html', not_found=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
