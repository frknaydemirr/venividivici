from sanic import Sanic
from server.common.check_schema import check_schema
from server.common.schemas.categories import get_category_schema, get_multiple_categories_schema, get_multiple_categories_with_stats_schema


def test_get_all_categories(sanic_instance: Sanic):
    request, response = sanic_instance.test_client.get("/categories/")

    assert response.status == 200
    assert check_schema(response.json, get_multiple_categories_schema)
    assert len(response.json) == 4


def test_get_categories_of_question(sanic_instance: Sanic):
    request, response = sanic_instance.test_client.get("/categories/question/13")

    assert response.status == 200
    assert check_schema(response.json, get_multiple_categories_schema)
    assert len(response.json) == 2

    for category in response.json:
        assert category["category-id"] in [1, 2]
        assert category["category-label"] in ["category_of_question1", "category_of_question2"]


def test_get_specific_category(sanic_instance: Sanic):
    request, response = sanic_instance.test_client.get("/categories/4")

    assert response.status == 200
    assert check_schema(response.json, get_category_schema)
    assert response.json["category-id"] == 4
    assert response.json["category-label"] == "specific_category"