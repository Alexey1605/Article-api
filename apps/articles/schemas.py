from marshmallow import Schema, fields, validates, ValidationError, validate
from marshmallow.validate import OneOf
from werkzeug.exceptions import UnprocessableEntity
from apps.articles.enums import ArticleColumnEnum


class PaginateSchema(Schema):
    page = fields.Integer()
    per_page = fields.Integer()


class ArticleSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    text = fields.String(required=True)
    created_date = fields.DateTime(dump_only=True, format='%Y-%m-%dT%H:%M:%S%z')
    updated_date = fields.DateTime(dump_only=True, format='%Y-%m-%dT%H:%M:%S%z')
    status = fields.String(dump_only=True)

    class Meta:
        ordered = True


class ArticleFilterSchema(PaginateSchema):
    filter_id = fields.Integer()
    filter_title = fields.String()
    filter_text = fields.String()
    filter_created_date = fields.DateTime()
    filter_updated_date = fields.DateTime()
    filter_status = fields.String()
    sort = fields.Str(validate=OneOf(ArticleColumnEnum.get_values()))
    sort_order = fields.String(validate=OneOf(['asc', 'desc']))


class ArticlePublicationSchema(Schema):
    is_published = fields.Bool(required=True)
