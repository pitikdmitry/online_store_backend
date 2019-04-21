from marshmallow import Schema, fields


class PostRequestSchema(Schema):
    category = fields.String(required=True)
    title = fields.String(required=True)
    text = fields.String(required=True)
    main_img = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    last_updated = fields.DateTime(required=True)


class CategoryResponseSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True)
