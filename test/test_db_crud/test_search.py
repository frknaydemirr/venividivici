from sqlalchemy.orm import Session
import pytest
from server.database.crud import Database
from datetime import datetime


def test_get_cities_matching_query(db_session: Session):
    db = Database(db_session)

    cities = db.get_cities_matching_query(query_string="ankara", limit=1, offset=0)

    assert cities[0]["city-id"] == 1


def test_get_countries_matching_query(db_session: Session):
    db = Database(db_session)

    countries = db.get_countries_matching_query(query_string="turkey", limit=1, offset=0)

    assert countries[0]["country-id"] == 1


def test_get_questions_matching_query(db_session: Session):
    db = Database(db_session)

    questions = db.get_questions_matching_query(query_string="Istanbul", limit=2, offset=0)

    correct_ids = [1, 6]

    assert questions[0]["question-id"] in correct_ids \
        and questions[1]["question-id"] in correct_ids