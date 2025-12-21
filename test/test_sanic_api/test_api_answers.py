from sanic import Sanic

entry_user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozfQ.umJRxDK7r36DCM6QxR-kSJFWLRJD2Kssk-t9GF84goQ" # user_id=3, username=entry_post_delete_user

def test_delete_answer(sanic_instance: Sanic):
    delete_req, delete_resp = sanic_instance.test_client.delete("/answers/2", headers={"Authorization": f"Bearer {entry_user_token}"})

    assert delete_resp.status == 200

    get_req, get_resp = sanic_instance.test_client.get("/answers/2", headers={"Authorization": f"Bearer {entry_user_token}"})

    assert get_resp.status == 404


def test_post_answer(sanic_instance: Sanic):
    post_req, post_resp = sanic_instance.test_client.post("/answers/", json={
        "question-id": 2,
        "answer-body": "test post answer body"
    }, headers={"Authorization": f"Bearer {entry_user_token}"})

    assert post_resp.status == 200
    new_answer_id = post_resp.json.get("answer-id")
    assert new_answer_id is not None

    get_req, get_resp = sanic_instance.test_client.get(f"/answers/{new_answer_id}", headers={"Authorization": f"Bearer {entry_user_token}"})

    assert get_resp.status == 200
    assert get_resp.json["answer-body"] == "test post answer body"


def test_get_answer(sanic_instance: Sanic):
    get_req, get_resp = sanic_instance.test_client.get("/answers/3")

    assert get_resp.status == 200
    assert get_resp.json["answer-body"] == "get answer body"


def test_get_answers_by_question(sanic_instance: Sanic):
    get_req, get_resp = sanic_instance.test_client.get("/answers/by-question/12?offset=0&limit=5")

    assert get_resp.status == 200
    assert len(get_resp.json) == 2

    accepted_bodies = ['first answer of question body', 'second answer of question body']
    for answer in get_resp.json:
        assert answer["question-id"] == 12
        assert answer["answer-body"] in accepted_bodies


def test_get_answers_by_user(sanic_instance: Sanic):    
    get_req, get_resp = sanic_instance.test_client.get("/answers/by-user/entry_get_user?offset=0&limit=10")

    assert get_resp.status == 200
    assert len(get_resp.json) == 3

    accepted_bodies = ['first answer of question body', 'second answer of question body', 'get answer body']
    for answer in get_resp.json:
        assert answer["username"] == "entry_get_user"
        assert answer["answer-body"] in accepted_bodies