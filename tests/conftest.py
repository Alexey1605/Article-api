from sqlalchemy import create_engine, insert
import pytest
from apps.articles.models import Article
from apps.core.app import create_app
from apps.core.extensions import db
from config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)


@pytest.fixture
def app():
    app = create_app('tests.config')
    with app.app_context():
        db.metadata.create_all(engine)
        yield app
        db.session.close()
        db.metadata.drop_all(engine)


@pytest.fixture
def test_client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def add_data_db(test_client):
    test_articles = [{"id": 1, "title": "book", "text": "about12 book", "created_date": "2017-02-22 22:22:22"},
                     {"id": 2, "title": "Car", "text": "test text 2", "status": "published"},
                     {"id": 3, "title": "flower", "text": "text333", "created_date": "2015-02-22 22:22:22"},
                     {"id": 4, "title": "boss", "text": "about12 house", "updated_date": "2011-01-11 22:22:22"},
                     {"id": 5, "title": "music", "text": "Lala lala text", "created_date": "2022-02-22 22:22:22"}]
    db.session.execute(
        insert(Article),
        test_articles,
    )
    db.session.commit()
