# TODO: Add questions by category endpoints
# TODO: Put upper limit on limit parameters
# TODO: Add await

from sanic import Sanic, Request, json, exceptions, file
from http import HTTPMethod

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from server.database.models import Base

from server.worker.module import setup_modules
from server.worker.db_setup import setup_db

DEFAULT = (
    "server.blueprints.answers",
    "server.blueprints.categories",
    "server.blueprints.cities",
    "server.blueprints.countries",
    "server.blueprints.login",
    "server.blueprints.questions",
    "server.blueprints.replies",
    "server.blueprints.search",
    "server.blueprints.subscriptions",
    "server.blueprints.users",
    "server.blueprints.votes",
)


def create_app(parameters = None) -> Sanic:
    module_names = DEFAULT

    app = Sanic(name="venividivici")
    db_url = "sqlite:///:memory:"


    if not app.config.get("CORS-ORIGINS"):
        app.config.CORS_ORIGINS = "*"

    
    setup_db(app_name="venividivici", db_url=db_url)
 
    setup_modules(app, *module_names)

    return app


def run_query_file(engine, file_path):
    with engine.begin() as connection:
        db_api_connection = connection.connection
        with open(file_path) as file:
            query = text(file.read())
            db_api_connection.executescript(query.text)


def create_test_app(parameters = None, external_session = None) -> Sanic: 
    module_names = DEFAULT

    app = Sanic(name="venividivici")
    db_url = ""

    if not external_session:
        api_engine = create_engine('sqlite:///:memory:')
        APISession = sessionmaker(bind=api_engine)
        Base.metadata.create_all(bind=api_engine)
        run_query_file(api_engine, 'test/helpers_test_insertions.sql')

        external_session = APISession(bind=api_engine)  

    if not app.config.get("CORS-ORIGINS"):
        app.config.CORS_ORIGINS = "*"

    setup_db(app_name="venividivici", db_url=db_url, external_session=external_session)
    
    setup_modules(app, *module_names)

    return app