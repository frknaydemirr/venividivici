from sanic import Sanic

def test_get_city(sanic_instance: Sanic):
    request, response = sanic_instance.test_client.get("/cities/10")
    
    assert response.status == 200
    assert response.json["city-name"] == 'get_city'


def test_get_cities_in_country(sanic_instance: Sanic):
    request, response = sanic_instance.test_client.get("/cities/by-country/8")
    
    assert response.status == 200
    assert len(response.json) == 1
    assert response.json[0]["city-name"] == 'get_city'