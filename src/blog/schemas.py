from marshmallow import Schema, fields, validate


class PostRequestSchema(Schema):
    category = fields.String(required=True)
    title = fields.String(required=True)
    text = fields.String(required=True)
    main_img = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    last_updated = fields.DateTime(required=True)


class PostResponseSchema(Schema):
    id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    title = fields.String(required=True)
    text = fields.String(required=True)
    main_img = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    last_updated = fields.DateTime(required=True)


class GetPostsRequestSchema(Schema):
    offset = fields.Integer(required=False, missing=0, validate=validate.Range(min=0))
    limit = fields.Integer(required=False, missing=0, validate=validate.Range(min=0, max=50))


class CategoryResponseSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True)
