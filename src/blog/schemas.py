from marshmallow import Schema, fields


class CategoryResponseSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True)
