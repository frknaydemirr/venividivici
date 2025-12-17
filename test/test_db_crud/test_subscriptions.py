from sqlalchemy.orm import Session
import pytest
from server.database.crud import Database
from datetime import datetime


def test_get_all_questions_from_subscriptions(db_session: Session):
    db = Database(db_session)

    questions = db.get_questions_from_subscriptions(
        user_id=1,
        offset=0,
        limit=4
    )

    correct_ids = [1, 3, 4, 6]

    assert questions[0]["question-id"] in correct_ids \
        and questions[1]["question-id"] in correct_ids \
        and questions[2]["question-id"] in correct_ids \
        and questions[3]["question-id"] in correct_ids


def test_get_all_cities_from_subscriptions(db_session: Session):
    db = Database(db_session)

    cities = db.get_subscribed_cities(
        user_id=1
    )

    correct_ids = [2, 4]

    assert cities[0]["city-id"] in correct_ids \
        and cities[1]["city-id"] in correct_ids


def test_get_all_countries_from_subscriptions(db_session: Session):
    db = Database(db_session)

    countries = db.get_subscribed_countries(
        user_id=3
    )

    correct_ids = [1, 3]

    assert countries[0]["country-id"] in correct_ids \
        and countries[1]["country-id"] in correct_ids


def test_post_subscribe_to_city(db_session: Session):
    db = Database(db_session)
    
    db.post_subscribe_city(
        user_id=1,
        city_id=4,
        subscription_type=False
    )

    cities = db.get_subscribed_cities(
        user_id=1
    )

    assert len(cities) == 1 and cities[0]["city-id"] == 2


def test_post_subscribe_to_country(db_session: Session):
    db = Database(db_session)
    
    db.post_subscribe_country(
        user_id=5,
        country_id=1,
        subscription_type=True
    )

    countries = db.get_subscribed_countries(
        user_id=5
    )

    assert len(countries) == 1 and countries[0]["country-id"] == 1