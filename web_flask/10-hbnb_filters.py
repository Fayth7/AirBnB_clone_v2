#!/usr/bin/python3
"""Starts a Flask web application"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Display the HBNB filters page"""

    states = storage.all("State").values()
    cities = storage.all("City").values()
    amenities = storage.all("Amenity").values()

    states = sorted(states, key=lambda x: x.name)
    cities = sorted(cities, key=lambda x: x.name)
    amenities = sorted(amenities, key=lambda x: x.name)

    return render_template(
        '10-hbnb_filters.html',
        states=states,
        cities=cities,
        amenities=amenities
    )


@app.teardown_appcontext
def teardown(exception):
    """Closes the current SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
