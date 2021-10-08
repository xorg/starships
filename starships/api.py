from flask import Blueprint
from flask import request, g, Blueprint, json, Response
from flask import jsonify
from flask import request
from marshmallow.exceptions import ValidationError
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
    return jsonify(starships)


@api_bp.route("/api/starships/<int:id>", methods=["GET"])
def show_starship(id):
    """View a single starship

    Returns:
        A single starship
    """
    starships = Starship.query.filter(Starship.id == id).first()
    return jsonify(starships)


@api_bp.route("/api/starships", methods=["POST"])
def create_starship():
    """Save a starship to database

    Returns:
        A single starship
    """
    req_data = request.get_json()
    print(starship_schema.load(req_data))
    try:
        data = starship_schema.load(req_data)
    except ValidationError as e:
        return response(400, e.messages)

    starship = Starship(data)

    # starship.additional_info = fetch_info(starship.model_id)

    # add random registration uuid if not given
    # if not starship.registration_number:
    #     starship.registration_number = 

    # commit object to database
    db.session.add(starship)
    db.session.commit()

    payload = starship_schema.dump(starship)
    return response(201, payload)


def response(status, data):
    """
    Helper function to create custom responses
    """

    return Response(
        mimetype="application/json",
        response=json.dumps(data),
        status=status
    )
