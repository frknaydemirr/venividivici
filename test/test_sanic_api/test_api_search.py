from sanic import Sanic

def test_get_search_cities(sanic_instance: Sanic):
    get_req, get_resp = sanic_instance.test_client.get("/search/cities/Search", params={"offset": 0, "limit": 1})

    assert get_resp.status == 200
    assert len(get_resp.json) == 1
    assert get_resp.json[0]["city-name"] == "Search City" \
        and get_resp.json[0]["city-id"] == 14


def test_get_search_countries(sanic_instance: Sanic):
    get_req, get_resp = sanic_instance.test_client.get("/search/countries/Search", params={"offset": 0, "limit": 1})

    assert get_resp.status == 200
    assert len(get_resp.json) == 1
    assert get_resp.json[0]["country-name"] == "Search Country" \
        and get_resp.json[0]["country-id"] == 12


def test_get_search_questions(sanic_instance: Sanic):
    get_req, get_resp = sanic_instance.test_client.get("/search/questions/Search", params={"offset": 0, "limit": 1})

    assert get_resp.status == 200
    assert len(get_resp.json) == 1
    assert get_resp.json[0]["question-id"] == 18 \
        and get_resp.json[0]["question-title"] == "search question title"
