import pytest
from apps.articles.enums import ArticleStatusEnum
from apps.articles.models import Article, Category
from apps.core.extensions import db


def test_add_article(test_client, add_categories_data_db):
    data = {"title": "test title", "text": "Lala lala", "category_id": "2"}
    response = test_client.post("/api/v1/articles/", json=data)
    assert response.status_code == 200
    created_article = db.session.query(Article).first()
    assert response.json.get('id') == created_article.id


def test_add_category(test_client):
    data = {"name": "test category", "description": "article category about test"}
    response = test_client.post("/api/v1/category/", json=data)
    assert response.status_code == 200
    created_category = db.session.query(Category).first()
    assert response.json.get('id') == created_category.id


def test_update_article(add_categories_data_db, add_data_db, test_client):
    body = {"title": "changed title", "text": "changed text", "category_id": "2"}
    data = test_client.put("/api/v1/articles/1/", json=body)
    assert data.status_code == 201
    updated_article: Article = db.session.query(Article).filter(Article.id == 1).first()
    assert data.json.get("title") == updated_article.title


def test_update_category(add_categories_data_db, test_client):
    body = {"name": "test category", "description": "article category about test"}
    data = test_client.put("/api/v1/category/1/", json=body)
    assert data.status_code == 201
    created_category: Category = db.session.query(Category).filter(Category.id == 1).first()
    assert data.json.get("name") == created_category.name


def test_change_article_not_found(add_categories_data_db, add_data_db, test_client):
    body = {"title": "test 123", "text": "Lala 123", "category_id": "2"}
    data = test_client.put("/api/v1/articles/99/", json=body)
    assert data.status_code == 404


def test_get_articles(add_categories_data_db, add_data_db,  test_client):
    data = test_client.get("/api/v1/articles/")
    assert data.status_code == 200


def test_check_by_id(add_categories_data_db, add_data_db, test_client):
    data = test_client.get("/api/v1/articles/3/")
    assert data.status_code == 200
    assert data.json.get('id') == 3


def test_check_by_category_name(add_categories_data_db, add_data_db, test_client):
    data = test_client.get("/api/v1/articles/3/")
    assert data.status_code == 200
    print(data.get_json())
    assert data.json.get('category_name') == 'flower'


@pytest.mark.parametrize('query_filter, result_count', [
    ({'filter_title': 'te'}, 2),
    ({"filter_text": "12"}, 3),
    ({"filter_created_date_start": "2016-02-22"}, 4),
    ({"filter_created_date_end": "2018-04-22"}, 2),
    ({"filter_updated_date_start": "2000-01-22"}, 1),
    ({"filter_status": "published"}, 1),
    ({"filter_text": "12", "filter_title": "te"}, 2),
    ({"filter_category_name": "flower"}, 1)])
def test_get_articles_with_filter(add_categories_data_db, add_data_db, test_client, query_filter, result_count):
    response = test_client.get("/api/v1/articles/", query_string=query_filter)
    assert len(response.json.get('items')) == result_count


@pytest.mark.parametrize('sort, sort_order, first_result', [
    ("id", "asc", 1),
    ("id", "desc", 5),
    ("created_date", None, 3)])
def test_get_articles_with_sorted(add_categories_data_db, add_data_db, test_client, sort, sort_order, first_result):
    response = test_client.get(f"/api/v1/articles/", query_string={'sort': sort, 'sort_order': sort_order})
    assert response.json.get('items')[0]['id'] == first_result


def test_delete_article(add_categories_data_db, add_data_db, test_client):
    response = test_client.delete('/api/v1/articles/1/')
    assert response.status_code == 204
    deleted_article = db.session.query(Article).filter(Article.id == 1).first()
    assert deleted_article.status == ArticleStatusEnum.DELETED.value


@pytest.mark.parametrize('is_published', [True, False])
def test_publish_article(add_categories_data_db, add_data_db, test_client, is_published):
    response = test_client.post('/api/v1/articles/1/publish/', json={'is_published': is_published})
    assert response.status_code == 200
    article = db.session.query(Article).filter(Article.id == 1).first()
    if is_published:
        assert article.status == ArticleStatusEnum.PUBLISHED.value
    else:
        assert article.status == ArticleStatusEnum.DRAFT.value


