from flask import Response

from apps.articles.models import Article
from apps.core.extensions import db


class ArticleManager:
    @classmethod
    def get_filter_articles(cls, args: dict):
        filter_title = args.get("filter_title")
        filter_text = args.get("filter_text")
        filter_created_date = args.get("filter_created_date")
        filter_updated_date = args.get("filter_updated_date")
        filter_status = args.get("filter_status")
        sort = args.get("sort")
        sort_order = args.get("sort_order")
        query = db.session.query(Article).filter(Article.status != 'deleted')

        if filter_title:
            query = query.filter(Article.title == filter_title)
        if filter_text:
            query = query.filter(Article.text == filter_text)
        if filter_created_date:
            query = query.filter(Article.created_date == filter_created_date)
        if filter_updated_date:
            query = query.filter(Article.updated_date == filter_updated_date)
        if filter_status:
            query = query.filter(Article.status == filter_status)
        if sort:
            sort_column = getattr(Article, sort)
            if sort_order:
                sort_column = sort_column.desc() if sort_order == 'desc' else sort_column.asc()
            query = query.order_by(sort_column)
        return query



