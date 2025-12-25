from sqlalchemy.orm import Session
import pytest
from server.database.crud import Database
from datetime import datetime


def test_get_specific_answer(db_session: Session):
    db = Database(db_session)

    answer = db.get_specific_answer(answer_id=2)

    assert answer == {
            "answer-id": 2,
            "answer-body": "Kadikoy has many great options; check reviews.",
            "username": "carol",
            "creation-time": datetime(2025, 12, 10, 13, 00),
            "question-id": 1
        }


def test_post_new_answer(db_session: Session):
    db = Database(db_session)

    answer_id = db.post_new_answer(
        user_id=2,
        question_id=1,
        answer_body="I recommend trying out 'Kebapçı İskender' in Beyoğlu."
    )

    assert db.get_specific_answer(answer_id=answer_id)


def test_get_reply_and_vote_counts_of_answer(db_session: Session):
    db = Database(db_session)

    counts = db.get_answer_vote_and_reply_counts(answer_id=7)

    assert counts == {
        "reply-count": 2,
        "vote-count": 3
    }


def test_get_answers_of_specific_question(db_session: Session):
    db = Database(db_session)

    answers = db.get_answers_of_specific_question(question_id=1, offset=0, limit=2)

    correct_ids = [1, 2]

    assert answers[0]["answer-id"] in correct_ids \
        and answers[1]["answer-id"] in correct_ids


def test_get_answers_of_specific_user(db_session: Session):
    db = Database(db_session)

    answers = db.get_answers_of_user(username="alice", offset=0, limit=3)

    correct_ids = [1, 5, 8]

    assert answers[0]["answer-id"] in correct_ids \
        and answers[1]["answer-id"] in correct_ids \
        and answers[2]["answer-id"] in correct_ids