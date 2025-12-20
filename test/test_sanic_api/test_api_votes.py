from sanic import Sanic

vote_user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyfQ.x2qTf1GqvXtZD94dnyh9BlRMgOIxB2-PxUn3EAaSuq8" # user_id=2, username=vote_user

def test_get_question_vote(sanic_instance: Sanic):
    request, response = sanic_instance.test_client.get("/votes/questions/1", headers={"Authorization": f"Bearer {vote_user_token}"})

    assert response.status == 200
    assert response.json["vote-type"] == True


def test_post_question_vote(sanic_instance: Sanic):
    post_req, post_resp = sanic_instance.test_client.post("/votes/questions/1", json={"vote-type": False}, headers={"Authorization": f"Bearer {vote_user_token}"})

    assert post_resp.status == 200

    get_req, get_resp = sanic_instance.test_client.get("/votes/questions/1", headers={"Authorization": f"Bearer {vote_user_token}"})

    assert get_resp.status == 200
    assert get_resp.json["vote-type"] == False


def test_delete_question_vote(sanic_instance: Sanic):
    delete_req, delete_resp = sanic_instance.test_client.delete("/votes/questions/1", headers={"Authorization": f"Bearer {vote_user_token}"})

    assert delete_resp.status == 200

    get_req, get_resp = sanic_instance.test_client.get("/votes/questions/1", headers={"Authorization": f"Bearer {vote_user_token}"})

    assert get_resp.status == 404


def test_get_answer_vote(sanic_instance: Sanic):
    request, response = sanic_instance.test_client.get("/votes/answers/1", headers={"Authorization": f"Bearer {vote_user_token}"})

    assert response.status == 200
    assert response.json["vote-type"] == True


def test_post_answer_vote(sanic_instance: Sanic):
    post_req, post_resp = sanic_instance.test_client.post("/votes/answers/1", json={"vote-type": False}, headers={"Authorization": f"Bearer {vote_user_token}"})

    assert post_resp.status == 200

    get_req, get_resp = sanic_instance.test_client.get("/votes/answers/1", headers={"Authorization": f"Bearer {vote_user_token}"})

    assert get_resp.status == 200
    assert get_resp.json["vote-type"] == False

def test_delete_answer_vote(sanic_instance: Sanic):
    delete_req, delete_resp = sanic_instance.test_client.delete("/votes/answers/1", headers={"Authorization": f"Bearer {vote_user_token}"})

    assert delete_resp.status == 200

    get_req, get_resp = sanic_instance.test_client.get("/votes/answers/1", headers={"Authorization": f"Bearer {vote_user_token}"})

    assert get_resp.status == 404

def test_get_reply_vote(sanic_instance: Sanic):
    request, response = sanic_instance.test_client.get("/votes/replies/1", headers={"Authorization": f"Bearer {vote_user_token}"})

    assert response.status == 200
    assert response.json["vote-type"] == True


def test_post_reply_vote(sanic_instance: Sanic):
    post_req, post_resp = sanic_instance.test_client.post("/votes/replies/1", json={"vote-type": False}, headers={"Authorization": f"Bearer {vote_user_token}"})

    assert post_resp.status == 200

    get_req, get_resp = sanic_instance.test_client.get("/votes/replies/1", headers={"Authorization": f"Bearer {vote_user_token}"})

    assert get_resp.status == 200
    assert get_resp.json["vote-type"] == False


def test_delete_reply_vote(sanic_instance: Sanic):
    delete_req, delete_resp = sanic_instance.test_client.delete("/votes/replies/1", headers={"Authorization": f"Bearer {vote_user_token}"})

    assert delete_resp.status == 200

    get_req, get_resp = sanic_instance.test_client.get("/votes/replies/1", headers={"Authorization": f"Bearer {vote_user_token}"})

    assert get_resp.status == 404