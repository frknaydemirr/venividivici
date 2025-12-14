from sqlalchemy.orm import Session
import pytest
from server.database.crud import Database
from datetime import datetime


def test_get_user_vote_for_question(db_session: Session):
    db = Database(db_session)

    vote = db.get_user_vote_for_question(user_id=4, question_id=1)

    assert vote == {
            "vote-type": False
        }

    
def test_post_user_vote_for_question(db_session: Session):
    db = Database(db_session)

    db.post_user_vote_for_question(
        user_id=1,
        question_id=5,
        vote_type=True
    )

    vote = db.get_user_vote_for_question(user_id=1, question_id=5)

    assert vote == {
            "vote-type": True
        }

    
def test_get_user_vote_for_answer(db_session: Session):
    db = Database(db_session)

    vote = db.get_user_vote_for_answer(user_id=2, answer_id=2)

    assert vote == {
            "vote-type": False
        }


def test_post_user_vote_for_answer(db_session: Session):
    db = Database(db_session)

    db.post_user_vote_for_answer(
        user_id=3,
        answer_id=5,
        vote_type=False
    )

    vote = db.get_user_vote_for_answer(user_id=3, answer_id=5)

    assert vote == {
            "vote-type": False
        }


def test_get_user_vote_for_reply(db_session: Session):
    db = Database(db_session)

    vote = db.get_user_vote_for_reply(user_id=1, reply_id=1)

    assert vote == {
            "vote-type": True
        }


def test_post_user_vote_for_reply(db_session: Session):
    db = Database(db_session)

    db.post_user_vote_for_reply(
        user_id=2,
        reply_id=1,
        vote_type=False
    )

    vote = db.get_user_vote_for_reply(user_id=2, reply_id=1)

    assert vote == {
            "vote-type": False
        }