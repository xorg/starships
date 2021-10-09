from marshmallow import fields, Schema



class AdditionalInfoSchema(Schema):
    id = fields.Int()
    info = fields.Str()


class StarshipSchema(Schema):
    """
    Starship schema
    """

    id = fields.Int(dump_only=True)
    nickname = fields.Str(required=True)
    owner = fields.Str(required=True)
    registration_number = fields.Str()
    model_id = fields.Int(required=True)
    additional_info = fields.Nested(AdditionalInfoSchema, dump_only=True)
