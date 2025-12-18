# TODO: Add questions by category endpoints
# TODO: Put upper limit on limit parameters
# TODO: Add await

from sanic import Sanic, text, Request, json, exceptions, file
from http import HTTPMethod

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

# Specify external session for testing purposes
def create_app(parameters = None, external_session = None) -> Sanic:
    module_names = DEFAULT

    app = Sanic(name="venividivici")
    db_url = "sqlite:///:memory:"


    if not app.config.get("CORS-ORIGINS"):
        app.config.CORS_ORIGINS = "*"

    if external_session:
        setup_db(app_name="venividivici", db_url=db_url, external_session=external_session)
    else:
        setup_db(app_name="venividivici", db_url=db_url)
 
    setup_modules(app, *module_names)

    return app