from sqlalchemy.orm import Session
import pytest
from server.database.crud import Database
from datetime import datetime


def test_post_question(db_session: Session):
    db = Database(db_session)
    
    question_id = db.post_new_question(
        user_id=1,
        city_id=1,
        question_title="Best time to visit Istanbul?",
        question_body="I am planning a trip to Istanbul and would like to know the best time to visit.",
        category_ids=[1, 2]
    )

    assert db.get_specific_question(question_id=question_id)


def test_get_specific_question(db_session: Session):
    db = Database(db_session)
    
    question = db.get_specific_question(question_id=1)

    assert question == {
            "question-id": 1,
            "question-title": "Best kebab in Istanbul?",
            "question-body": "Looking for kebab places in Istanbul.",
            "username": "bob",
            "creation-time": datetime(2025, 12, 10, 10, 15),
            "city-id": 2,
            "country-id": 1
        }


def test_get_answer_and_vote_counts_of_question(db_session: Session):
    db = Database(db_session)

    counts = db.get_question_answer_and_vote_counts(question_id=6)

    assert counts == {
        "answer-count": 3,
        "vote-count": 2
    }


def test_get_most_answered_questions(db_session: Session):
    db = Database(db_session)

    questions = db.get_most_answered_questions(offset=0, limit=1)

    assert questions[0]["question-id"] == 6


def test_get_most_answered_questions_of_city(db_session: Session):
    db = Database(db_session)

    questions = db.get_most_answered_questions_in_city(city_id=2, offset=0, limit=2)

    assert questions[0]["question-id"] == 6 \
        and questions[1]["question-id"] == 1


def test_get_most_answered_questions_of_country(db_session: Session):
    db = Database(db_session)

    questions = db.get_most_answered_questions_in_country(country_id=1, offset=0, limit=3)

    assert questions[0]["question-id"] == 6 \
        and questions[1]["question-id"] == 1 \
        and questions[2]["question-id"] == 2


def test_get_recent_questions(db_session: Session):
    db = Database(db_session)

    questions = db.get_recent_questions(offset=0, limit=3)

    assert questions[0]["question-id"] == 6 \
        and questions[1]["question-id"] == 4 \
        and questions[2]["question-id"] == 2

    
def test_get_recent_questions_of_city(db_session: Session):
    db = Database(db_session)

    questions = db.get_recent_questions_of_city(city_id=2, offset=0, limit=1)

    assert questions[0]["question-id"] == 6


def test_get_recent_questions_of_country(db_session: Session):
    db = Database(db_session)

    questions = db.get_recent_questions_of_country(country_id=1, offset=0, limit=2)

    assert questions[1]["question-id"] == 2


def test_get_questions_by_user(db_session: Session):
    db = Database(db_session)

    questions = db.get_questions_of_user(username="bob", offset=0, limit=2)

    correct_ids = [1, 6]

    assert questions[0]["question-id"] in correct_ids\
        and questions[1]["question-id"] in correct_ids