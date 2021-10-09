import uuid
import requests
from flask import Blueprint
from flask import Response
from flask import jsonify
from flask import json
from flask import request
from marshmallow.exceptions import ValidationError
from requests.models import HTTPError
from .models import Starship, AdditionalInfo, db
from .schemas import StarshipSchema

api_bp = Blueprint("api", __name__)
starship_schema = StarshipSchema()


@api_bp.route("/api/starships", methods=["GET"])
def list_starship():
    """View list of all owned starships

    Returns:
        A list of all starships stored in database
    """
    starships = Starship.query.all()
    data = starship_schema.dump(starships, many=True)
    return jsonify(data)


@api_bp.route("/api/starships/<int:id>", methods=["GET"])
def show_starship(id):
    """View a single starship

    Returns:
        A single starship
    """
    starship = Starship.query.filter(Starship.id == id).first()
    data = starship_schema.dump(starship)
    if not starship:
        return response(404, "Starship not found")
    return jsonify(data)


@api_bp.route("/api/starships", methods=["POST"])
def create_starship():
    """Save a starship to database

    Returns:
        A single starship
    """
    # check if request has the correct media type
    if not request.headers.get("Content-Type") == "application/json":
        return response(415, None)

    req_data = request.get_json()

    # try to validate json with schema
    try:
        data = starship_schema.load(req_data)
    except ValidationError as e:
        return response(400, e.messages)

    starship = Starship(data)

    # try to fetch info from database
    info = AdditionalInfo.query.filter(
        AdditionalInfo.id == starship.model_id).first()
    if info:
        starship.additional_info = info
    else:
        try:
            info = fetch_info(starship.model_id)
            starship.additional_info = info
        except HTTPError as e:
            return response(e.response.status_code, e.response.json())

    # add random registration uuid if not given
    if not starship.registration_number:
        starship.registration_number = str(uuid.uuid4())

    # commit object to database
    db.session.add(starship)
    db.session.commit()

    payload = starship_schema.dump(starship)
    return response(201, payload)


def fetch_info(id):
    """Fetches additional starship info from external api"""
    print(f"Fetching info for model #{id}")
    resp = requests.get(f"https://swapi.dev/api/starships/{id}")

    # raise an exception if there"s an http error
    resp.raise_for_status()

    data = resp.content
    info = AdditionalInfo(id=id, info=data)
    db.session.add(info)
    db.session.commit()
    return info


def response(status, data):
    """
    Helper function to create custom responses
    """

    return Response(mimetype="application/json",
                    response=json.dumps(data),
                    status=status)
