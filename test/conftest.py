# TODO: Add unauthenticated tests to API
# TODO: Add negative tests to API (404 etc.)
# TODO: Add tests for counts and filtering to API
# TODO: Add delete helpers tests for CRUD
# TODO: Add Redis tests

import pytest

from server.database.models import Base
from server.database.crud import Database
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from sanic import Sanic
from server.server import create_test_app

def run_query_file(engine, file_path):
    with engine.begin() as connection:
        db_api_connection = connection.connection
        with open(file_path) as file:
            query = text(file.read())
            db_api_connection.executescript(query.text)


helpers_engine = create_engine('sqlite:///:memory:')
HelpersSession = sessionmaker(bind=helpers_engine)
Base.metadata.create_all(bind=helpers_engine)
run_query_file(helpers_engine, 'test/helpers_test_insertions.sql')

@pytest.fixture(scope='function')
def db_session():
    # Setup
    connection = helpers_engine.connect()
    transaction = connection.begin()

    session = HelpersSession(bind=connection)

    yield session

    # Teardown
    session.close()
    transaction.rollback()
    connection.close()


api_engine = create_engine('sqlite:///:memory:')
APISession = sessionmaker(bind=api_engine)
Base.metadata.create_all(bind=api_engine)
run_query_file(api_engine, 'test/api_test_insertions.sql')

@pytest.fixture(scope='module')
def sanic_instance():
    # Setup
    connection = api_engine.connect()
    transaction = connection.begin()

    session = APISession(bind=connection)
    
    app = create_test_app("venividivici", external_session=session)

    yield app

    # Teardown
    session.close()
    transaction.rollback()
    connection.close()