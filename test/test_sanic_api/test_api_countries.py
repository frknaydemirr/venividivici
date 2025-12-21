from sanic import Sanic

# TODO: Add get all countries

def test_get_country(sanic_instance: Sanic):
    request, response = sanic_instance.test_client.get("/countries/8")
    assert response.status == 200
    assert response.json["country-name"] == "get_country"