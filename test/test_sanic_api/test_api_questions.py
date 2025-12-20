from sanic import Sanic

entry_user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozfQ.umJRxDK7r36DCM6QxR-kSJFWLRJD2Kssk-t9GF84goQ" # user_id=3, username=entry_post_delete_user

def test_delete_question(sanic_instance: Sanic):
    delete_req, delete_resp = sanic_instance.test_client.delete("/questions/2", headers={"Authorization": f"Bearer {entry_user_token}"})

    assert delete_resp.status == 200

    get_req, get_resp = sanic_instance.test_client.get("/questions/2", headers={"Authorization": f"Bearer {entry_user_token}"})

    assert get_resp.status == 404


def test_post_question(sanic_instance: Sanic):
    post_req, post_resp = sanic_instance.test_client.post("/questions/", json={
        "city-id": 2,
        "question-title": "test post question title",
        "question-body": "test post question body",
        "category-ids": []
    }, headers={"Authorization": f"Bearer {entry_user_token}"})

    assert post_resp.status == 200
    new_question_id = post_resp.json.get("question-id")
    assert new_question_id is not None

    get_req, get_resp = sanic_instance.test_client.get(f"/questions/{new_question_id}", headers={"Authorization": f"Bearer {entry_user_token}"})

    assert get_resp.status == 200
    assert get_resp.json["question-title"] == "test post question title"
    assert get_resp.json["question-body"] == "test post question body"