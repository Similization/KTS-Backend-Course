from marshmallow import Schema, fields


class AdminSchema(Schema):
    email = fields.Str(required=True, attribute='email')
    # password = fields.Str(required=True, attribute='password')
