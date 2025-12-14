from sqlalchemy.orm import Session
import pytest
from server.database.crud import Database
from datetime import datetime


def test_get_user_info(db_session: Session):
    db = Database(db_session)

    user_info = db.get_user_info(username="alice")

    assert user_info == {
            "username": "alice",
            "creation-time": datetime(2025, 11, 20, 9, 10),
            "city-id": 1
        }