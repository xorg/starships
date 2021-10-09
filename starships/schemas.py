import json
from marshmallow import fields, Schema


class JsonField(fields.Str):
    """Field that stores a json blob and serializes it to a python dict
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return json.loads(value)


class AdditionalInfoSchema(Schema):
    id = fields.Int()
    info = JsonField()


class StarshipSchema(Schema):
    id = fields.Int(dump_only=True)
    nickname = fields.Str(required=True)
    owner = fields.Str(required=True)
    registration_number = fields.Str()
    model_id = fields.Int(required=True)
    additional_info = fields.Nested(AdditionalInfoSchema, dump_only=True)
