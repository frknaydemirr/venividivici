from sanic import Sanic
from server.common.check_schema import check_schema
from server.common.schemas.countries import get_country_schema

# TODO: Add get all countries

def test_get_country(sanic_instance: Sanic):
    request, response = sanic_instance.test_client.get("/countries/8")
    
    assert response.status == 200
    assert check_schema(response.json, get_country_schema)
    assert response.json["country-name"] == "get_country"