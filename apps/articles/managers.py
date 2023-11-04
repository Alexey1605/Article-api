from sqlalchemy import or_

from apps.articles.models import Article
from apps.core.extensions import db


class ArticleManager:
    @classmethod
    def get_filter_articles(cls, args: dict):
        filter_title = args.get("filter_title")
        filter_text = args.get("filter_text")
        filter_created_date_start = args.get("filter_created_date_start")
        filter_created_date_end = args.get("filter_created_date_end")
        filter_updated_date_start = args.get("filter_updated_date_start")
        filter_updated_date_end = args.get("filter_updated_date_end")
        filter_status = args.get("filter_status")
        filter_category_name = args.get("filter_category_name")
        filter_query = args.get("filter_query")
        sort = args.get("sort")
        sort_order = args.get("sort_order")
        query = db.session.query(Article).filter(Article.status != 'deleted')

        if filter_title:
            query = query.filter(Article.title.ilike(f'%{filter_title}%'))
        if filter_text:
            query = query.filter(Article.text.ilike(f'%{filter_text}%'))
        if filter_created_date_start:
            query = query.filter(Article.created_date >= filter_created_date_start)
        if filter_created_date_end:
            query = query.filter(Article.created_date <= filter_created_date_end)
        if filter_updated_date_start:
            query = query.filter(Article.updated_date >= filter_updated_date_start)
        if filter_updated_date_end:
            query = query.filter(Article.updated_date <= filter_updated_date_end)
        if filter_status:
            query = query.filter(Article.status.in_(filter_status))
        if filter_category_name:
            query = query.filter(Article.category_name == filter_category_name)
            print(query)

        if filter_query:
            query = query.filter(or_(Article.text.ilike(f'%{filter_query}%'),
                                     Article.title.ilike(f'%{filter_query}%')))
        if sort:
            sort_column = getattr(Article, sort)
            if sort_order:
                sort_column = sort_column.desc() if sort_order == 'desc' else sort_column.asc()
            query = query.order_by(sort_column)
        return query
