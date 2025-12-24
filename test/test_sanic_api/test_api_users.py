from sanic import Sanic

def test_get_user_info(sanic_instance: Sanic):
    get_req, get_resp = sanic_instance.test_client.get("/users/info_user/info")

    assert get_resp.status == 200
    assert get_resp.json["username"] == "info_user"
    assert get_resp.json["city-id"] == 10
    assert get_resp.json["creation-time"] == "20251129 184000"


def test_register_user(sanic_instance: Sanic):
    post_req, post_resp = sanic_instance.test_client.post("/users/register", json={
        "username": "registered_user",
        "full-name": "registered User",
        "e-mail-addr": "register_user@test.com",
        "password": "Reg1sterP@ssw0rd",
        "city-id": 8
    })

    assert post_resp.status == 200

    get_req, get_resp = sanic_instance.test_client.get("/users/registered_user/info")
    assert get_resp.status == 200
    assert get_resp.json["username"] == "registered_user"
    assert get_resp.json["city-id"] == 8
