from flask import jsonify, Response, request
from flask.json import dumps
from webargs.flaskparser import use_args
from apps.articles.enums import ArticleStatusEnum
from apps.articles.managers import ArticleManager
from apps.articles.models import Article
from apps.articles.schemas import ArticleSchema, ArticlePublicationSchema, ArticleFilterSchema
from apps.articles.utils import create_response
from apps.core.extensions import db
from flask import Blueprint


article_bp = Blueprint("article", __name__, url_prefix='/articles/')


@article_bp.route("", methods=['POST'])
def create():
    data = request.get_json()
    schema = ArticleSchema()
    cleaned_data = schema.load(data)
    article = Article(**cleaned_data)
    db.session.add(article)
    db.session.commit()
    return create_response(schema.dumps(article), status_code=200)


@article_bp.route("<int:pk>", methods=['PUT'])
def update_article(pk=None):
    article = db.session.query(Article).filter(Article.id == pk).first()
    data = request.get_json()
    schema = ArticleSchema()
    updated_data = schema.load(data)
    db.session.query(Article).filter(Article.id == pk).update(updated_data)
    db.session.commit()
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


@article_bp.route("/<int:id>", methods=['GET'])
def get_id_articles(id):
    article = db.session.query(Article).get_or_404(id)
    serializer = ArticleSchema()
    data = serializer.dump(article)
    return create_response(dumps(data), status_code=200)


@article_bp.route("<int:id>", methods=['DELETE'])
def delete_article(id):
    article = db.session.query(Article).get_or_404(id)
    article.status = ArticleStatusEnum.DELETED.value
    db.session.commit()
    return create_response(status_code=204)


@article_bp.route("<int:id>/publication", methods=['POST'])
def publish_article(id):
    article = db.session.query(Article).get_or_404(id)
    data = request.get_json()
    schema = ArticlePublicationSchema()
    cleaned_data = schema.load(data)
    article.status = ArticleStatusEnum.PUBLISHED.value if cleaned_data[
        'is_published'] else ArticleStatusEnum.DRAFT.value
    db.session.commit()
    return create_response()
