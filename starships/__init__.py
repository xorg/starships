import os

from flask import Flask


def create_app():
    """ Create and configure the app. Initialize blueprints.
    """
    app = Flask(__name__)
    
    app_env = os.environ.get("FLASK_ENV")
    app.config.from_object(f'starships.config.{app_env.capitalize()}')

    return app

def register_blueprints():
    from .api import api_bp

app = create_app()
