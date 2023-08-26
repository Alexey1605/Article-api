from flask import Flask
from apps.articles.views import article_bp
from apps.core.extensions import db, migrate


def create_app(config_object='config.config'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(article_bp)
    return app
