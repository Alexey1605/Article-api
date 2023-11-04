from marshmallow import Schema, fields
from marshmallow.validate import OneOf
from webargs.fields import DelimitedList
from apps.articles.enums import ArticleColumnEnum


class PaginateSchema(Schema):
    page = fields.Integer()
    per_page = fields.Integer()


class ArticleSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    text = fields.String(required=True)
    created_date = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S')
    updated_date = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S')
    status = fields.String(dump_only=True)
    category_id = fields.Integer(required=True)
    category_name = fields.String(dump_only=True, attribute='category.name')

    class Meta:
        ordered = True


class ArticleFilterSchema(PaginateSchema):
    filter_id = fields.Integer()
    filter_title = fields.String()
    filter_text = fields.String()
    filter_created_date_start = fields.Date()
    filter_created_date_end = fields.Date()
    filter_updated_date_start = fields.Date()
    filter_updated_date_end = fields.Date()
    filter_status = DelimitedList(fields.Str())
    filter_query = fields.String()
    filter_category_name = fields.String()
    sort = fields.Str(validate=OneOf(ArticleColumnEnum.get_values()))
    sort_order = fields.String(validate=OneOf(['asc', 'desc']))


class CategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)


class ArticlePublicationSchema(Schema):
    is_published = fields.Bool(required=True)
