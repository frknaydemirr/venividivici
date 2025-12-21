from sanic import Sanic

def test_get_user_info(sanic_instance: Sanic):
    get_req, get_resp = sanic_instance.test_client.get("/users/info_user/info")

    assert get_resp.status == 200
    assert get_resp.json["username"] == "info_user"
    assert get_resp.json["city-id"] == 10
    assert get_resp.json["creation-time"] == "20251129 184000"