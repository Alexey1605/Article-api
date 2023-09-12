import paginate
from flask import jsonify, Response, request
from flask.json import dumps
from sqlalchemy import desc
from webargs import fields
from webargs.flaskparser import use_args
from marshmallow import ValidationError
from apps.articles.enums import ArticleStatusEnum
from apps.articles.models import Article
from apps.articles.schemas import ArticleSchema, ArticlePublicationSchema, ArticleFilterSchema
from apps.core.extensions import db
from flask import Blueprint
from apps.exceptions import NotFoundError, Notimplemented, InternalServerError, RequestEntityTooLarge, BadRequest


article_bp = Blueprint("article", __name__, url_prefix='/articles/')


@article_bp.route("", methods=['POST'])
def create():
    data = request.get_json()
    schema = ArticleSchema()
    cleaned_data = schema.load(data)
    article = Article(**cleaned_data)
    db.session.add(article)
    db.session.commit()
    return Response(schema.dumps(article), status=201, mimetype='application/json')


@article_bp.route("<int:pk>", methods=['PUT'])
def update_article(pk=None):
    article = db.session.query(Article).filter(Article.id == pk).first()
    data = request.get_json()
    schema = ArticleSchema()
    updated_data = schema.load(data)
    db.session.query(Article).filter(Article.id == pk).update(updated_data)
    db.session.commit()
    data = ArticleSchema().dump(article)
    return Response(dumps(data), status=201)


@article_bp.route("", methods=['GET'])
@use_args(ArticleFilterSchema(), location="query")
def get_all_articles(args):
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
    return Response(dumps(data), status=201, mimetype='application/json')


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
