import os

from flask import Flask
from .api import api_bp
from .models import db


def create_app():
    """ Create and configure the app. Initialize blueprints.
    """
    app = Flask(__name__)

    app_env = os.environ.get("FLASK_ENV")
    app.config.from_object(f"starships.config.{app_env.capitalize()}")

    # initialize api blueprint
    app.register_blueprint(api_bp)

    # initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


app = create_app()
