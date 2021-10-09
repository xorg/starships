
import pytest
from dotenv import load_dotenv

load_dotenv()

from starships import create_app
from starships.models import db


@pytest.fixture
def client():
    app = create_app()
    app.config.from_object("starships.config.Test")

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            db.create_all()

        yield client


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/api/starships')
    assert b"[]" in rv.data
