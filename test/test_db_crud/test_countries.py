from sqlalchemy.orm import Session
import pytest
from server.database.crud import Database
from datetime import datetime


def test_get_all_countries(db_session: Session):
    db = Database(db_session)
    
    countries = db.get_all_countries()

    assert countries == [
            {
                "country-id": 1,
                "country-name": "Turkey"
            },
            {
                "country-id": 2,
                "country-name": "USA"
            },
            {
                "country-id": 3,
                "country-name": "Germany"
            }
        ]


def test_get_qa_counts_for_country(db_session: Session):
    db = Database(db_session)
    
    counts = db.get_country_question_and_answer_counts(country_id=1)

    assert counts == {
            "question-count": 3,
            "answer-count": 6
        }


def test_get_specific_country(db_session: Session):
    db = Database(db_session)
    
    country = db.get_specific_country(country_id=2)

    assert country == {
            "country-id": 2,
            "country-name": "USA",
            "url": None,
            "info": "Test country: USA"
        }


def test_get_most_conquered_countries(db_session: Session):
    db = Database(db_session)
    
    countries = db.get_most_conquered_countries(limit=1)

    assert countries == [
            {
                "country-id": 1,
                "country-name": "Turkey",
                "url": None,
                "info": "Test country: Turkey"
            }
        ]
