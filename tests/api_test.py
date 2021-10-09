import pytest
import os
from dotenv import load_dotenv

load_dotenv()

from starships import create_app
from starships.models import db, Starship
from starships.api import fetch_info
from starships.schemas import StarshipSchema


@pytest.fixture
def client():
    app = create_app()
    app.config.from_object("starships.config.Test")

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            db.create_all()
        yield client

    db_path = app.config["SQLALCHEMY_DATABASE_URI"].split("sqlite:///")[-1]
    os.unlink(db_path)


def test_empty_db(client):
    """Start with a blank database."""

    resp = client.get("/api/starships")
    assert b"[]" in resp.data

    resp = client.get("/api/starships/1")
    assert 404 == resp.status_code


def test_create_starships(client):
    """Test post endpoint """
    # test with wrong headers
    correct_body = """
    {
        "nickname": "Falcy",
        "owner": "Han Solo",
        "model_id": 10
    }"""
    wrong_headers = {"Content-Type": "application/text"}
    resp = client.post("/api/starships",
                       data=correct_body,
                       headers=wrong_headers)
    assert 415 == resp.status_code

    # test correct headers
    correct_headers = {"Content-Type": "application/json"}
    resp = client.post("/api/starships",
                       data=correct_body,
                       headers=correct_headers)
    assert 201 == resp.status_code

    # check if additional info has been correctly fetched
    assert "Millennium Falcon" == resp.json["additional_info"]["info"]["name"]

    # test wrong json headers
    wrong_body = """
    {
        "nickname": "Falcy",
        "owner": 234324,
        "model_id": 10,
        "registration_number": "lksjfir-23jlkj-djflk3-l23j4k"
    }"""
    correct_headers = {"Content-Type": "application/json"}
    resp = client.post("/api/starships",
                       data=wrong_body,
                       headers=correct_headers)
    assert 400 == resp.status_code
    assert {"owner": ["Not a valid string."]} == resp.json

    # test not existing starship in swapi
    not_found_body = """
    {
        "nickname": "Testy",
        "owner": "Luke Codewalker",
        "model_id": 1
    }"""
    resp = client.post("/api/starships",
                       data=not_found_body,
                       headers=correct_headers)
    assert resp.status_code == 404

    # test if starships have been correctly added to db
    assert len(Starship.query.all()) == 1


def test_list_starships(client):
    """ Test get endpoints
    """
    # create starship in db
    body = """
    {
        "nickname": "Testibus",
        "owner": "Darth Vader",
        "model_id": 5
    }"""
    correct_headers = {"Content-Type": "application/json"}
    resp = client.post("/api/starships", data=body, headers=correct_headers)

    resp = client.get("/api/starships")
    assert resp.status_code == 200
    assert len(resp.json) == 1

    resp = client.get("/api/starships/1")
    assert resp.status_code == 200
    assert resp.json["nickname"] == "Testibus"
