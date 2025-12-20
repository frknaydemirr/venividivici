from sanic import Sanic

entry_user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozfQ.umJRxDK7r36DCM6QxR-kSJFWLRJD2Kssk-t9GF84goQ" # user_id=3, username=entry_post_delete_user

def test_delete_reply(sanic_instance: Sanic):
    delete_req, delete_resp = sanic_instance.test_client.delete("/replies/2", headers={"Authorization": f"Bearer {entry_user_token}"})

    assert delete_resp.status == 200

    get_req, get_resp = sanic_instance.test_client.get("/replies/2", headers={"Authorization": f"Bearer {entry_user_token}"})

    assert get_resp.status == 404


def test_post_reply(sanic_instance: Sanic):
    post_req, post_resp = sanic_instance.test_client.post("/replies/", json={
        "answer-id": 2,
        "reply-body": "test post reply body"
    }, headers={"Authorization": f"Bearer {entry_user_token}"})

    assert post_resp.status == 200
    new_reply_id = post_resp.json.get("reply-id")
    assert new_reply_id is not None

    get_req, get_resp = sanic_instance.test_client.get(f"/replies/{new_reply_id}", headers={"Authorization": f"Bearer {entry_user_token}"})

    assert get_resp.status == 200
    assert get_resp.json["reply-body"] == "test post reply body"