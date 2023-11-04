from flask import request
from flask.json import dumps
from webargs.flaskparser import use_args
from apps.articles.enums import ArticleStatusEnum
from apps.articles.managers import ArticleManager
from apps.articles.models import Article, Category
from apps.articles.schemas import ArticleSchema, ArticlePublicationSchema, ArticleFilterSchema, CategorySchema
from apps.articles.utils import create_response, provide_session
from flask import Blueprint


article_bp = Blueprint("article", __name__, url_prefix='/api/v1/articles/')
category_bp = Blueprint("category", __name__, url_prefix='/api/v1/category/')


@article_bp.route("", methods=['POST'])
@provide_session
def create(session):
    data = request.get_json()
    schema = ArticleSchema()
    cleaned_data = schema.load(data)
    article = Article(**cleaned_data)
    session.add(article)
    session.commit()
    return create_response(schema.dumps(article), status_code=200)


@article_bp.route("<int:pk>/", methods=['PUT'])
@provide_session
def update_article(session, pk=None):
    article = session.query(Article).get_or_404(pk)
    data = request.get_json()
    schema = ArticleSchema()
    updated_data = schema.load(data)
    session.query(Article).filter(Article.id == pk).update(updated_data)
    session.commit()
    data = ArticleSchema().dump(article)
    return create_response(dumps(data), status_code=201)


@article_bp.route("", methods=['GET'])
@use_args(ArticleFilterSchema(), location="query")
def get_all_articles(args):
    query = ArticleManager.get_filter_articles(args)
    page = args.get('page')
    per_page = args.get('per_page')
    paginate_articles = query.paginate(page=page, per_page=per_page)
    serializer = ArticleSchema(many=True)
    data = serializer.dump(paginate_articles)

    data = {
        "total_count": paginate_articles.total,
        "page": paginate_articles.page,
        "items": data
    }
    return create_response(dumps(data), status_code=200)


@article_bp.route("/<int:id>/", methods=['GET'])
@provide_session
def get_id_articles(session, id):
    article = session.query(Article).get_or_404(id)
    serializer = ArticleSchema()
    data = serializer.dump(article)
    return create_response(dumps(data), status_code=200)


@article_bp.route("<int:id>/", methods=['DELETE'])
@provide_session
def delete_article(session, id):
    article = session.query(Article).get_or_404(id)
    article.status = ArticleStatusEnum.DELETED.value
    session.commit()
    return create_response(status_code=204)


@article_bp.route("<int:id>/publish/", methods=['POST'])
@provide_session
def publish_article(session, id):
    article = session.query(Article).get_or_404(id)
    data = request.get_json()
    schema = ArticlePublicationSchema()
    cleaned_data = schema.load(data)
    article.status = ArticleStatusEnum.PUBLISHED.value if cleaned_data[
        'is_published'] else ArticleStatusEnum.DRAFT.value
    session.commit()
    return create_response()


@category_bp.route("", methods=['POST'])
@provide_session
def create_category(session):
    data = request.get_json()
    schema = CategorySchema()
    cleaned_data = schema.load(data)
    category = Category(**cleaned_data)
    session.add(category)
    session.commit()
    return create_response(schema.dumps(category), status_code=200)


@category_bp.route("", methods=['GET'])
@provide_session
def get_all_categories(session):
    category = session.query(Category).all()
    serializer = CategorySchema(many=True)
    data = serializer.dump(category)
    return create_response(dumps(data), status_code=200)


@category_bp.route("<int:pk>/", methods=['PUT'])
@provide_session
def update_category(session, pk=None):
    category = session.query(Category).get_or_404(pk)
    data = request.get_json()
    schema = CategorySchema()
    updated_data = schema.load(data)
    session.query(Category).filter(Category.id == pk).update(updated_data)
    session.commit()
    data = CategorySchema().dump(category)
    return create_response(dumps(data), status_code=201)


@category_bp.route("<int:id>/", methods=['DELETE'])
@provide_session
def delete_category(session, id):
    category = session.query(Category).get_or_404(id)
    session.delete(category)
    session.commit()
    return create_response(status_code=204)
