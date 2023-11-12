import pytest


from apps.core.extensions import db
from apps.news.enums import NewsStatusEnum
from apps.news.models import News


def test_add_news(test_client):
    data = {"title": "world cup", "description": "Argentina win this tournament", "edition": "Marca"}
    response = test_client.post("/api/v1/news/", json=data)
    assert response.status_code == 200
    created_news = db.session.query(News).first()
    assert response.json.get('news_id') == created_news.news_id


def test_update_news(add_news_data_db, test_client):
    body = {"title": "test", "description": "About test", "edition": "Sky Sports"}
    data = test_client.put("/api/v1/news/1/", json=body)
    assert data.status_code == 201
    updated_news: News = db.session.query(News).filter(News.news_id == 1).first()
    assert data.json.get("title") == updated_news.title


def test_change_news_not_found(add_news_data_db, test_client):
    body = {"title": "test", "description": "About test", "edition": "Sky Sports"}
    data = test_client.put("/api/v1/news/99/", json=body)
    assert data.status_code == 404


def test_get_news(add_news_data_db, test_client):
    data = test_client.get("/api/v1/news/")
    assert data.status_code == 200


def test_get_news_by_id(add_news_data_db, test_client):
    data = test_client.get("/api/v1/news/3/")
    assert data.status_code == 200
    assert data.json.get('news_id') == 3


@pytest.mark.parametrize('query_filter, result_count', [
    ({'filter_title': 'world'}, 2),
    ({"filter_description": "12"}, 2),
    ({"filter_created_date_start": "2016-02-22"}, 3),
    ({"filter_created_date_end": "2018-04-22"}, 2),
    ({"filter_updated_date_start": "1800-01-22"}, 0),
    ({"filter_status": "published"}, 1),
    ({"filter_edition": "BBC"}, 1),
    ({"filter_description": "12", "filter_title": "12"}, 2)])
def test_get_news_with_filter(add_news_data_db, test_client, query_filter, result_count):
    response = test_client.get("/api/v1/news/", query_string=query_filter)
    assert len(response.json.get('items')) == result_count


@pytest.mark.parametrize('sort, sort_order, first_result', [
    ("news_id", "asc", 1),
    ("news_id", "desc", 5),
    ("created_date", None, 3)])
def test_get_news_with_sorted(add_news_data_db, test_client, sort, sort_order, first_result):
    response = test_client.get(f"/api/v1/news/", query_string={'sort': sort, 'sort_order': sort_order})
    assert response.json.get('items')[0]['news_id'] == first_result


def test_delete_news(add_news_data_db, test_client):
    response = test_client.delete('/api/v1/news/1/')
    assert response.status_code == 204
    deleted_news = db.session.query(News).filter(News.news_id == 1).first()
    assert deleted_news.status == NewsStatusEnum.DELETED.value


@pytest.mark.parametrize('is_published', [True, False])
def test_publish_news(add_news_data_db, test_client, is_published):
    response = test_client.post('/api/v1/news/1/publish/', json={'is_published': is_published})
    assert response.status_code == 200
    news = db.session.query(News).filter(News.news_id == 1).first()
    if is_published:
        assert news.status == NewsStatusEnum.PUBLISHED.value
    else:
        assert news.status == NewsStatusEnum.DRAFT.value