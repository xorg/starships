from flask import Blueprint
from flask import request, g, Blueprint, json, Response
from flask import jsonify
from flask import request
from .models import Starship, AdditionalInfo


api_bp = Blueprint("api", __name__)


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


@api_bp.route("/api/starships", methods=["GET"])
def create_starship(id):
    """Save a starship to database

    Returns:
        A single starship
    """
    req_data = request.get_json()

    return jsonify(req_data)
