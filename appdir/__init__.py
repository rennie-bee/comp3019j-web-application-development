from flask import Flask, render_template
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

# The programme writing of appdir/__init__.py studies the instruction in Book
# "FLASK Web Development: Developing Web Applications with Python, Second Edition"
# This __init__ plays as a factory method. It supports creating multiple application instances.
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    # the parameter config_name transits the config settings from config.py and we use from_object to import that
    app.config.from_object(config[config_name])
    # use init_app() to initialize previously created extended objects
    config[config_name].init_app(app)

    db.init_app(app)

    # register blueprint for main directory
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # register blueprint for auth directory
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # if app.debug:
    #     from werkzeug.debug import DebuggedApplication
    #     app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
    return app
