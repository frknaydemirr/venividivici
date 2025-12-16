import pytest
from server.database.models import Base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:')

def run_query_file(engine, file_path):
    with engine.begin() as connection:
        db_api_connection = connection.connection
        with open(file_path) as file:
            query = text(file.read())
            db_api_connection.executescript(query.text)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)
run_query_file(engine, 'test/test_insertions.sql')

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