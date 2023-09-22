#!/usr/bin/python3
"""
Script that starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import environ

app = Flask(__name__)
app.url_map.strict_slashes = False

# Tear down SQLAlchemy session


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


@app.route('/hbnb')
def hbnb_filters():
    """
    Display HTML page
    """
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    return render_template('100-hbnb.html',
                           states=states,
                           amenities=amenities,
                           places=places)


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = environ.get('HBNB_API_PORT', 5000)
    app.run(host=host, port=int(port))
