import pytest
from apps.articles.enums import ArticleStatusEnum
from apps.articles.models import Article
from apps.core.extensions import db


def test_add_article(test_client):
    data = {"title": "test title", "text": "Lala lala"}
    response = test_client.post("/articles/", json=data)
    assert response.status_code == 200
    created_article = db.session.query(Article).first()
    assert response.json.get('id') == created_article.id


def test_update_article(add_data_db, test_client):
    body = {"title": "changed title", "text": "changed text"}
    data = test_client.put("/articles/1", json=body)
    assert data.status_code == 201
    updated_article: Article = db.session.query(Article).filter(Article.id == 1).first()
    assert data.json.get("title") == updated_article.title


def test_change_article_not_found(add_data_db, test_client):
    body = {"title": "test 123", "text": "Lala 123"}
    data = test_client.put("/articles/99", json=body)
    assert data.status_code == 404


def test_get_articles(add_data_db, test_client):
    data = test_client.get("/articles/")
    print(data.get_json())
    assert data.status_code == 200


def test_check_by_id(add_data_db, test_client):
    data = test_client.get("/articles/3")
    print(data.get_json())
    assert data.status_code == 200
    assert data.json.get('id') == 3


@pytest.mark.parametrize('query_filter, result_count', [
    ({'filter_title': 'Bo'}, 2),
    ({"filter_text": "te"}, 3),
    ({"filter_created_date_start": "2016-02-22"}, 4),
    ({"filter_created_date_end": "2018-04-22"}, 2),
    ({"filter_updated_date_start": "2000-01-22"}, 1),
    ({"filter_status": "published"}, 1),
    ({"filter_text": "bo", "filter_title": "bo"}, 2)])
def test_get_articles_with_filter(add_data_db, test_client, query_filter, result_count):
    response = test_client.get("/articles/", query_string=query_filter)
    assert len(response.json.get('items')) == result_count


@pytest.mark.parametrize('sort, first_result', [
    ("?sort_order=asc&sort=id", 1),
    ("?sort_order=desc&sort=id", 5),
    ("?sort=created_date", 5)])
def test_get_articles_with_sorted(add_data_db, test_client, sort, first_result):
    response = test_client.get(f"/articles/{sort}")
    assert response.json.get('items')[0]['id'] == first_result


def test_delete_article(add_data_db, test_client):
    response = test_client.delete('/articles/1')
    assert response.status_code == 204
    deleted_article = db.session.query(Article).filter(Article.id == 1).first()
    assert deleted_article.status == ArticleStatusEnum.DELETED.value


@pytest.mark.parametrize('is_published', [True, False])
def test_publish_article(add_data_db, test_client, is_published):
    response = test_client.post('/articles/1/publish', json={'is_published': is_published})
    assert response.status_code == 200
    article = db.session.query(Article).filter(Article.id == 1).first()
    if is_published:
        assert article.status == ArticleStatusEnum.PUBLISHED.value
    else:
        assert article.status == ArticleStatusEnum.DRAFT.value

