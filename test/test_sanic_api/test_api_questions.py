from sanic import Sanic
from server.common.check_schema import check_schema
from server.common.schemas.questions import get_multiple_questions_schema, get_question_schema, get_new_question_id_schema

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
    assert check_schema(post_resp.json, get_new_question_id_schema)
    new_question_id = post_resp.json.get("question-id")
    assert new_question_id is not None

    get_req, get_resp = sanic_instance.test_client.get(f"/questions/{new_question_id}", headers={"Authorization": f"Bearer {entry_user_token}"})

    assert get_resp.status == 200
    assert get_resp.json["question-title"] == "test post question title"
    assert get_resp.json["question-body"] == "test post question body"


def test_get_question(sanic_instance: Sanic):
    get_req, get_resp = sanic_instance.test_client.get("/questions/11")

    assert get_resp.status == 200
    assert check_schema(get_resp.json, get_question_schema)
    assert get_resp.json["question-title"] == "get question title"


def test_get_questions_of_user(sanic_instance: Sanic):
    get_req, get_resp = sanic_instance.test_client.get("/questions/by-user/questions_user")

    assert get_resp.status == 200
    assert check_schema(get_resp.json, get_multiple_questions_schema)
    assert len(get_resp.json) == 2
    
    for question in get_resp.json:
        assert question["question-id"] in [14, 15]