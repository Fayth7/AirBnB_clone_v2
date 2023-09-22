#!/usr/bin/python3
"""
Script to start a Flask web application that displays a list of states
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from os import environ
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Route to display a list of states from the database
    """
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)

    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def close_db(error):
    """
    Closes the database at the end of the request.
    """
    storage.close()


if __name__ == "__main__":
    host = environ.get("HBNB_API_HOST", '0.0.0.0')
    port = environ.get("HBNB_API_PORT", '5000')
    app.run(host=host, port=port, threaded=True)
