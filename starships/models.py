from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Starship(db.Model):
    """Owned starship"""

    def __init__(self, data):
        """This method allows the creation of a Starship model
        directly from schema validated data
        """
        self.nickname = data.get("nickname")
        self.owner = data.get("owner")
        self.model_id = data.get("model_id")
        self.registration_number = data.get("registration_number")

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(80))
    owner = db.Column(db.String(80))
    registration_number = db.Column(db.String(80))
    model_id = db.Column(db.Integer,
                         db.ForeignKey("additional_info.id"),
                         nullable=False)


class AdditionalInfo(db.Model):
    """Starship model information cache"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    starships = db.relationship(Starship, backref="additional_info", lazy=True)
    info = db.Column(db.Text())
