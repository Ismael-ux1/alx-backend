#!/usr/bin/env python3
""" Flask app """
from flask import Flask, render_template
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


class Config:
    """ Config class for setting up Babel """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_local():
    """
    Function to determine the best maching language from the,
    client's Accept-language header
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """ Function to get the timezone for date formatting """
    return "UTC"


@app.route('/')
def index():
    """ Defines the route for root URL ("/") """
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run(debug=True)
