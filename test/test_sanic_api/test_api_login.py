from sanic import Sanic
import json

def test_get_token(sanic_instance: Sanic):
    data = {
        "username": "alice",
        "password": "md5_like_hash_aaaaaaaaaaaaaaa"
    }
    request, response = sanic_instance.test_client.post("/login", data=json.dumps(data))

    assert response.json["token"] == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ.JXFeJSGHt24GYetVrWlq5FJXwoa8YRu_Zrx89AzI8Qs"


def test_invalid_password_get_token(sanic_instance: Sanic):
    data = {
        "username": "alice",
        "password": "wrong_password"
    }
    request, response = sanic_instance.test_client.post("/login", data=json.dumps(data))

    assert response.status == 401


def test_invalid_username_get_token(sanic_instance: Sanic):
    data = {
        "username": "non_existent_user",
        "password": "md5_like_hash_aaaaaaaaaaaaaaa"
    }
    request, response = sanic_instance.test_client.post("/login", data=json.dumps(data))

    assert response.status == 401