# TODO: Add questions by category endpoints
# TODO: Put upper limit on limit parameters

from sanic import Sanic, Request, json, exceptions, file
from http import HTTPMethod

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from server.database.models import Base

from server.worker.module import setup_modules
from server.worker.db_setup import setup_db

from server.worker.setup_logger import setup_logger
import logging

from sanic_redis import SanicRedis

from dotenv import load_dotenv
import os

load_dotenv('.env')

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
    app_name = os.getenv("APP_NAME")

    app = Sanic(name=app_name)

    db_url = os.getenv("DATABASE_URL")
    setup_db(app_name=app_name, db_url=db_url)

    setup_logger(app_name=app_name, log_level=logging.INFO)

    if not app.config.get("CORS-ORIGINS"):
        app.config.CORS_ORIGINS = "*"

    setup_modules(app, *module_names)

    # Redis Configuration
    app.config.update({
        "REDIS": os.getenv("REDIS_URL"),
    })

    redis = SanicRedis(app)
    redis.init_app(app)

    return app


################ TESTING APP CREATION ###############

def run_query_file(engine, file_path):
    with engine.begin() as connection:
        db_api_connection = connection.connection
        with open(file_path) as file:
            query = text(file.read())
            db_api_connection.executescript(query.text)


def create_test_app(parameters = None, external_session = None) -> Sanic: 
    module_names = DEFAULT

    app_name = os.getenv("APP_NAME")

    app = Sanic(name=app_name)
    db_url = ""

    if not external_session:
        api_engine = create_engine(os.getenv('API_TEST_DATABASE_URL'))
        APISession = sessionmaker(bind=api_engine)
        Base.metadata.create_all(bind=api_engine)
        run_query_file(api_engine, os.getenv('API_TEST_SQL_PATH'))

        external_session = APISession(bind=api_engine)  

    if not app.config.get("CORS-ORIGINS"):
        app.config.CORS_ORIGINS = "*"

    setup_db(app_name=app_name, db_url=db_url, external_session=external_session)
    
    setup_modules(app, *module_names)

    # Redis Configuration
    app.config.update({
        "REDIS": os.getenv("REDIS_TEST_URL"),
    })

    redis = SanicRedis(app)
    redis.init_app(app)

    return app