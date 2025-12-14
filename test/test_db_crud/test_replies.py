from sqlalchemy.orm import Session
import pytest
from server.database.crud import Database
from datetime import datetime


def test_get_replies_of_specific_answer(db_session: Session):
    db = Database(db_session)

    replies = db.get_replies_of_specific_answer(answer_id=1, offset=0, limit=2)

    correct_ids = [1, 2]

    assert replies[0]["reply-id"] in correct_ids \
        and replies[1]["reply-id"] in correct_ids


def test_get_specific_reply(db_session: Session):
    db = Database(db_session)

    reply = db.get_specific_reply(reply_id=1)

    assert reply == {
            "reply-id": 1,
            "answer-id": 1,
            "username": "bob",
            "reply-body": "Thanks! Any specific place name?",
            "creation-time": datetime(2025, 12, 10, 12, 30)
        }


def test_post_new_reply(db_session: Session):
    db = Database(db_session)

    reply_id = db.post_new_reply(
        user_id=3,
        answer_id=1,
        reply_body="I second that recommendation!"
    )

    assert db.get_specific_reply(reply_id=reply_id)


def test_get_vote_counts_of_reply(db_session: Session):
    db = Database(db_session)

    counts = db.get_vote_counts_for_specific_reply(reply_id=1)

    assert counts == {
        "vote-count": 2
    }


def test_get_replies_of_specific_user(db_session: Session):
    db = Database(db_session)

    replies = db.get_replies_of_user(username="alice", offset=0, limit=2)

    correct_ids = [3, 5]

    assert replies[0]["reply-id"] in correct_ids \
        and replies[1]["reply-id"] in correct_ids