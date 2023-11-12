from sqlalchemy import insert
import pytest
from apps.articles.models import Article, Category
from apps.core.app import create_app
from apps.core.extensions import db
from apps.news.models import News
from test_data import test_articles, test_categories, test_news


@pytest.fixture
def app():
    app = create_app('tests.config')
    with app.app_context():
        db.create_all()
        yield app
        db.session.close()
        db.drop_all()


@pytest.fixture
def test_client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def add_data_db(test_client):
    db.session.execute(
        insert(Article),
        test_articles,
    )
    db.session.commit()


@pytest.fixture
def add_categories_data_db(test_client):
    db.session.execute(
        insert(Category),
        test_categories,
    )
    db.session.commit()


@pytest.fixture
def add_news_data_db(test_client):
    db.session.execute(
        insert(News),
        test_news,
    )
    db.session.commit()
