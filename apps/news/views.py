from json import dumps

from flask import Blueprint, request
from webargs.flaskparser import use_args


from apps.articles.utils import provide_session, create_response
from apps.news.enums import NewsStatusEnum
from apps.news.managers import NewsManager
from apps.news.models import News
from apps.news.schemas import NewsSchema, NewsFilterSchema, NewsPublicationSchema


news_bp = Blueprint("news", __name__, url_prefix='/api/v1/news/')


@news_bp.route("", methods=['POST'])
@provide_session
def create_news(session):
    data = request.get_json()
    schema = NewsSchema()
    cleaned_data = schema.load(data)
    news = News(**cleaned_data)
    session.add(news)
    session.commit()
    return create_response(schema.dumps(news), status_code=200)


@news_bp.route("<int:pk>/", methods=['PUT'])
@provide_session
def update_news(session, pk=None):
    news = session.query(News).get_or_404(pk)
    data = request.get_json()
    schema = NewsSchema()
    updated_data = schema.load(data)
    session.query(News).filter(News.news_id == pk).update(updated_data)
    session.commit()
    data = NewsSchema().dump(news)
    return create_response(dumps(data), status_code=201)


@news_bp.route("", methods=['GET'])
@use_args(NewsFilterSchema(), location="query")
def get_all_news(args):
    query = NewsManager.get_filter_news(args)
    page = args.get('page')
    per_page = args.get('per_page')
    paginate_news = query.paginate(page=page, per_page=per_page)
    serializer = NewsSchema(many=True)
    data = serializer.dump(paginate_news)

    data = {
        "total_count": paginate_news.total,
        "page": paginate_news.page,
        "items": data
    }
    return create_response(dumps(data), status_code=200)


@news_bp.route("/<int:id>/", methods=['GET'])
@provide_session
def get_id_news(session, id):
    news = session.query(News).get_or_404(id)
    serializer = NewsSchema()
    data = serializer.dump(news)
    return create_response(dumps(data), status_code=200)


@news_bp.route("<int:id>/", methods=['DELETE'])
@provide_session
def delete_news(session, id):
    news = session.query(News).get_or_404(id)
    news.status = NewsStatusEnum.DELETED.value
    session.commit()
    return create_response(status_code=204)


@news_bp.route("<int:id>/publish/", methods=['POST'])
@provide_session
def publish_news(session, id):
    news = session.query(News).get_or_404(id)
    data = request.get_json()
    schema = NewsPublicationSchema()
    cleaned_data = schema.load(data)
    news.status = NewsStatusEnum.PUBLISHED.value if cleaned_data[
        'is_published'] else NewsStatusEnum.DRAFT.value
    session.commit()
    return create_response()
