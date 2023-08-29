import paginate
from flask import jsonify, Response, request
from flask.json import dumps

from apps.articles.enums import ArticleStatusEnum
from apps.articles.models import Article
from apps.articles.schemas import ArticleSchema, ArticlePublicationSchema
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
    return Response(schema.dumps(article), status=201)


@article_bp.route("<int:pk>", methods=['PUT'])
def update_article(pk=None):
    article = db.session.query(Article).filter(Article.id == pk).first()
    data = request.get_json()
    schema = ArticleSchema()
    updated_data = schema.load(data)
    db.session.query(Article).filter(Article.id == pk).update(updated_data)
    db.session.commit()
    data = ArticleSchema().dump(article)
    return Response(schema.dumps(data), status=201)


@article_bp.route("", methods=['GET'])
def get_all_articles():
    page = request.args.get('page',1,type=int)
    per_page = request.args.get('per_page',5,type=int)
    articles = db.session.query(Article).filter_by().paginate(page=page, per_page=per_page)
    serializer = ArticleSchema(many=True)
    data = serializer.dump(articles)
    return Response(dumps(data), 200)


@article_bp.route("/<int:id>", methods=['GET'])
def get_id_articles(id):
    article = db.session.query(Article).get_or_404(id)
    serializer = ArticleSchema()
    data = serializer.dump(article)
    return jsonify(data), 200


@article_bp.route("<int:id>", methods=['DELETE'])
def delete_article(id):
    article = db.session.query(Article).get_or_404(id)
    article.status = ArticleStatusEnum.DELETED.value
    db.session.commit()
    return Response(status=204)


@article_bp.route("<int:id>/publication", methods=['POST'])
def publish_article(id):
    article = db.session.query(Article).get_or_404(id)
    data = request.get_json()
    schema = ArticlePublicationSchema()
    cleaned_data = schema.load(data)
    article.status = ArticleStatusEnum.PUBLISHED.value if cleaned_data[
        'is_published'] else ArticleStatusEnum.DRAFT.value
    db.session.commit()
    return Response(status=200)
