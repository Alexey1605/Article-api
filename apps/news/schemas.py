from marshmallow import Schema, fields
from marshmallow.validate import OneOf
from webargs.fields import DelimitedList

from apps.articles.schemas import PaginateSchema
from apps.news.enums import NewsColumnEnum


class NewsSchema(Schema):
    news_id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    created_date = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S')
    updated_date = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S')
    edition = fields.String(required=True)
    status = fields.String(dump_only=True)

    class Meta:
        ordered = True


class NewsFilterSchema(PaginateSchema):
    filter_news_id = fields.Integer()
    filter_title = fields.String()
    filter_description = fields.String()
    filter_created_date_start = fields.Date()
    filter_created_date_end = fields.Date()
    filter_updated_date_start = fields.Date()
    filter_updated_date_end = fields.Date()
    filter_edition = fields.String()
    filter_status = DelimitedList(fields.Str())
    filter_query = fields.String()
    sort = fields.Str(validate=OneOf(NewsColumnEnum.get_values()))
    sort_order = fields.String(validate=OneOf(['asc', 'desc']))


class NewsPublicationSchema(Schema):
    is_published = fields.Bool(required=True)
