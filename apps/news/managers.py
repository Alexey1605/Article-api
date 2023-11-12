from sqlalchemy import or_


from apps.core.extensions import db
from apps.news.models import News


class NewsManager:
    @classmethod
    def get_filter_news(cls, args: dict):
        filter_title = args.get("filter_title")
        filter_description = args.get("filter_description")
        filter_created_date_start = args.get("filter_created_date_start")
        filter_created_date_end = args.get("filter_created_date_end")
        filter_updated_date_start = args.get("filter_updated_date_start")
        filter_updated_date_end = args.get("filter_updated_date_end")
        filter_edition = args.get("filter_edition")
        filter_status = args.get("filter_status")
        filter_query = args.get("filter_query")
        sort = args.get("sort")
        sort_order = args.get("sort_order")
        query = db.session.query(News).filter(News.status != 'deleted')

        if filter_title:
            query = query.filter(News.title.ilike(f'%{filter_title}%'))
        if filter_description:
            query = query.filter(News.description.ilike(f'%{filter_description}%'))
        if filter_created_date_start:
            query = query.filter(News.created_date >= filter_created_date_start)
        if filter_created_date_end:
            query = query.filter(News.created_date <= filter_created_date_end)
        if filter_updated_date_start:
            query = query.filter(News.updated_date >= filter_updated_date_start)
        if filter_updated_date_end:
            query = query.filter(News.updated_date <= filter_updated_date_end)
        if filter_edition:
            query = query.filter(News.edition.ilike(f'%{filter_edition}%'))
        if filter_status:
            query = query.filter(News.status.in_(filter_status))

        if filter_query:
            query = query.filter(or_(News.description.ilike(f'%{filter_query}%'),
                                     News.title.ilike(f'%{filter_query}%')))
        if sort:
            sort_column = getattr(News, sort)
            if sort_order:
                sort_column = sort_column.desc() if sort_order == 'desc' else sort_column.asc()
            query = query.order_by(sort_column)
        return query
