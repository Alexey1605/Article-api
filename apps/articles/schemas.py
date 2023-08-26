from marshmallow import Schema, fields


class ArticleSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    text = fields.String(required=True)


class ArticlePublicationSchema(Schema):
    is_published = fields.Bool(required=True)