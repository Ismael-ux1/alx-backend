#!/usr/bin/env python3
""" Flask app """
from flask import Flask, render_template, request
from flask_babel import Babel
from flask import g
import pytz

app = Flask(__name__)
babel = Babel(app)


class Config:
    """ Config class for setting up Babel """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """
    Function to get a user based on the 'login_as' parameter in the request
    """
    user_id = request.args.get('login_as')
    if user_id is not None and int(user_id) in users:
        return users[int(user_id)]
    return None


@app.before_request
def before_request():
    """ Function to be excuted before all other functions """
    g.user = get_user()


@babel.localeselector
def get_locale():
    """
    Function to determine the best maching language,
    The order of priority list is:
    1. Locale from URL parameters
    2. Locale from user settings
    3. Locale from request header
    4. Default locale
    """
    # Locale from URL parameters
    if 'locale' in request.args:
        locale = request.args.get('locale')
        if locale in app.config['LANGUAGES']:
            return locale

    # Locale from user settings
    if hasattr(g, 'user') and g.user is not None:
        user_locale = g.user['settings']['locale'] \
            if 'settings' in g.user and 'locale' in g.user['settings'] \
            else None
        if user_locale and user_locale in app.config['LANGUAGES']:
            return user_locale

    # Locale from request header
    header_locale = request.accept_languages.best_match(app.config
                                                        ['LANGUAGES'])
    if header_locale:
        return header_locale

    # Default locale
    return 'en'


@babel.timezoneselector
def get_timezone():
    """
    Function to get the timezone for date formatting
    The order of priority is:
    1. Timezone from URL parameters
    2. Timezone from user settings
    3. Default to UTC
    """
    # Timezone from URL parameters
    if 'timezone' in request.args:
        timezone = request.args.get('timezone')
        try:
            pytz.timezone(timezone)
            return timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Timezone from user settings
    if hasattr(g, 'user') and g.user is not None:
        user_timezone = g.user['settings']['timezone'] \
                if 'settings' in g.user and 'timezone' in g.user['settings'] \
                else None
        try:
            pytz.timezone(user_timezone)
            return user_timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    # Defualt timezone
    return "UTC"


@app.route('/')
def index():
    """ Defines the route for root URL ("/") """
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run(debug=True)
