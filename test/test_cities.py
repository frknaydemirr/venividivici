from sqlalchemy.orm import Session
import pytest
from server.database.crud import Database

def test_get_specific_city(db_session: Session):
    db = Database(db_session)
    
    # Assuming a city with ID 1 exists in the test database
    city = db.get_specific_city(city_id=1)

    assert city == {
            "city-id": 1,
            "city-name": "Ankara",
            "url": None,
            "info": "Test city: Ankara"
        }

def test_get_qa_counts_for_city(db_session: Session):
    db = Database(db_session)
    
    # Assuming a city with ID 1 exists in the test database
    counts = db.get_city_question_and_answer_counts(city_id=2)

    assert counts == {
            "question-count": 2,
            "answer-count": 5
        }

def test_get_cities_in_country(db_session: Session):
    db = Database(db_session)
    
    cities = db.get_cities_in_specific_country(country_id=1, limit=10, offset=0)

    assert cities == [
            {
                "city-id": 1,
                "city-name": "Ankara",
                "url": None,
                "info": "Test city: Ankara"
            },
            {
                "city-id": 2,
                "city-name": "Istanbul",
                "url": None,
                "info": "Test city: Istanbul"
            }
        ]

def test_get_most_conquered_cities(db_session: Session):
    db = Database(db_session)
    
    cities = db.get_most_conquered_cities(limit=3)

    assert cities == [
            {
                "city-id": 2,
                "city-name": "Istanbul",
                "url": None,
                "info": "Test city: Istanbul"
            },
            {
                "city-id": 3,
                "city-name": "New York",
                "url": None,
                "info": "Test city: New York"

            },
            {
                "city-id": 1,
                "city-name": "Ankara",
                "url": None,
                "info": "Test city: Ankara"
            }
        ]

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
