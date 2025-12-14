from sqlalchemy.orm import Session
import pytest
from server.database.crud import Database
from datetime import datetime


def test_get_specific_category(db_session: Session):
    db = Database(db_session)

    category = db.get_specific_category(category_id=1)

    assert category == {
            "category-id": 1,
            "category-label": "Travel"
        }


def test_get_all_categories(db_session: Session):
    db = Database(db_session)

    categories = db.get_all_categories()

    assert categories == [
            {
                "category-id": 1,
                "category-label": "Travel"
            },
            {
                "category-id": 2,
                "category-label": "Food"
            },
            {
                "category-id": 3,
                "category-label": "Tech"
            },
            {
                "category-id": 4,
                "category-label": "Study"
            }
        ]


def test_get_categories_of_question(db_session: Session):
    db = Database(db_session)

    categories = db.get_categories_of_question(question_id=1)

    correct_ids = [1, 2]

    assert categories[0]["category-id"] in correct_ids \
        and categories[1]["category-id"] in correct_ids


def test_get_all_categories_in_city(db_session: Session):
    db = Database(db_session)

    categories = db.get_all_categories_of_city_with_stats(city_id=2)


    assert [
        {"category-id": 1, "category-label": "Travel", "question-count": 2, "answer-count": 5 },
        {"category-id": 2, "category-label": "Food",   "question-count": 1, "answer-count": 2 },
        {"category-id": 3, "category-label": "Tech",   "question-count": 1, "answer-count": 3 },
        {"category-id": 4, "category-label": "Study",  "question-count": 0, "answer-count": 0 }
]


def test_get_all_categories_in_country(db_session: Session):
    db = Database(db_session)

    categories = db.get_all_categories_of_country_with_stats(country_id=1)


    assert categories == [
        {"category-id": 1, "category-label": "Travel", "question-count": 2, "answer-count": 5 },
        {"category-id": 2, "category-label": "Food",   "question-count": 1, "answer-count": 2 },
        {"category-id": 3, "category-label": "Tech",   "question-count": 2, "answer-count": 4 },
        {"category-id": 4, "category-label": "Study",  "question-count": 0, "answer-count": 0 }
]