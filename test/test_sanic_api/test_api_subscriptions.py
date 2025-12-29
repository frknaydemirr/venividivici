from sanic import Sanic

sub_user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0fQ.Ozo3pC25He-KNTfyXt72Hz3DIcO2vNX39Nx9v9KDhzU"  # user_id=4, username=sub_user

def test_get_questions_from_subs(sanic_instance: Sanic):
    get_req, get_resp = sanic_instance.test_client.get("/subscriptions/questions", headers={"Authorization": f"Bearer {sub_user_token}"})
    
    assert get_resp.status == 200
    assert len(get_resp.json) == 6


def test_get_subscribed_cities(sanic_instance: Sanic):
    get_req, get_resp = sanic_instance.test_client.get("/subscriptions/cities", headers={"Authorization": f"Bearer {sub_user_token}"})

    assert get_resp.status == 200
    assert len(get_resp.json) == 1
    assert get_resp.json[0]["city-id"] == 3


def test_post_subscribe_city(sanic_instance: Sanic):
    post_req, post_resp = sanic_instance.test_client.post("/subscriptions/cities", json={"city-id": 7, "subscription-type": True},
        headers={"Authorization": f"Bearer {sub_user_token}"})

    assert post_resp.status == 200

    get_req, get_resp = sanic_instance.test_client.get("/subscriptions/cities", headers={"Authorization": f"Bearer {sub_user_token}"})

    assert get_resp.status == 200
    assert len(get_resp.json) == 2

    unsubscribe_req, unsubscribe_resp = sanic_instance.test_client.post("/subscriptions/cities", json={"city-id": 7, "subscription-type": False}, headers={"Authorization": f"Bearer {sub_user_token}"})

    assert unsubscribe_resp.status == 200

    final_get_req, final_get_resp = sanic_instance.test_client.get("/subscriptions/cities", headers={"Authorization": f"Bearer {sub_user_token}"})

    assert final_get_resp.status == 200
    assert len(final_get_resp.json) == 1


def test_get_subscribed_countries(sanic_instance: Sanic):
    get_req, get_resp = sanic_instance.test_client.get("/subscriptions/countries", headers={"Authorization": f"Bearer {sub_user_token}"})

    assert get_resp.status == 200
    assert len(get_resp.json) == 1
    assert get_resp.json[0]["country-id"] == 4


def test_post_subscribe_country(sanic_instance: Sanic):
    post_req, post_resp = sanic_instance.test_client.post("/subscriptions/countries", json={"country-id": 5, "subscription-type": True},
        headers={"Authorization": f"Bearer {sub_user_token}"})

    assert post_resp.status == 200

    get_req, get_resp = sanic_instance.test_client.get("/subscriptions/countries", headers={"Authorization": f"Bearer {sub_user_token}"})

    assert get_resp.status == 200
    assert len(get_resp.json) == 2

    unsubscribe_req, unsubscribe_resp = sanic_instance.test_client.post("/subscriptions/countries", json={"country-id": 5, "subscription-type": False}, headers={"Authorization": f"Bearer {sub_user_token}"})

    assert unsubscribe_resp.status == 200

    final_get_req, final_get_resp = sanic_instance.test_client.get("/subscriptions/countries", headers={"Authorization": f"Bearer {sub_user_token}"})

    assert final_get_resp.status == 200
    assert len(final_get_resp.json) == 1