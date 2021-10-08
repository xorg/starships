from marshmallow import fields, Schema, INCLUDE


class StarshipSchema(Schema):
    """
    Starship schema
    """

    id = fields.Int(dump_only=True)
    nickname = fields.Str(required=True)
    owner = fields.Str(required=True)
    registration_number = fields.Str()
    model_id = fields.Int(required=True)
    additional_info = fields.Raw(dump_only=True)

    class Meta:
        unknown = INCLUDE
