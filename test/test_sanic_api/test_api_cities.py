from sanic import Sanic
from server.common.check_schema import check_schema
from server.common.schemas.cities import get_city_schema, get_multiple_cities_schema

def test_get_city(sanic_instance: Sanic):
    request, response = sanic_instance.test_client.get("/cities/10")
    
    assert response.status == 200
    assert check_schema(response.json, get_city_schema)
    assert response.json["city-name"] == 'get_city'


def test_get_cities_in_country(sanic_instance: Sanic):
    request, response = sanic_instance.test_client.get("/cities/by-country/8")
    
    assert response.status == 200
    assert check_schema(response.json, get_multiple_cities_schema)
    assert len(response.json) == 1
    assert response.json[0]["city-name"] == 'get_city'