from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


@dataclass
class Starship(db.Model):
    """Owned starship"""

    id: int
    nickname: str
    owner: str
    registration_number: str
    model_id: int
    additional_info: "AdditionalInfo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(80))
    owner = db.Column(db.String(80))
    registration_number = db.Column(db.String(80))
    model_id = db.Column(db.Integer)
    model = db.relationship(
        "Model",
        backref=db.backref("starships", lazy=True),
    )


@dataclass
class AdditionalInfo(db.Model):
    """Starship model information cache"""

    id: int
    model_id: int
    info: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_id = db.Column(db.Integer, db.ForeignKey("starship.id"), nullable=False)
    info = db.Column(db.Text())
