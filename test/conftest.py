import pytest
from server.database.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.db')
Session = sessionmaker(bind=engine)

@pytest.fixture(scope='function')
def db_session():
    # Setup
    connection = engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)

    yield session

    # Teardown
    session.close()
    transaction.rollback()
    connection.close()