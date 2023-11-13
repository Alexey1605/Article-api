from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from apps.articles.views import article_bp, category_bp
from apps.core.error_handlers import handle_exceptions
from apps.core.extensions import db, migrate
from apps.news.views import news_bp
from openapi import openapi

SWAGGER_URL = '/api/docs'
API_URL = 'http://127.0.0.1:5000/docs/openapi.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL)


def create_app(config_object='config.config'):
    app = Flask(__name__)
    CORS(app, support_credentials=True)
    app.config.from_object(config_object)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_error_handler(Exception, handle_exceptions)
    app.register_blueprint(article_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(news_bp)
    app.add_url_rule('/docs/openapi.json', 'openapi', view_func=openapi)
    app.register_blueprint(swaggerui_blueprint)
    return app
