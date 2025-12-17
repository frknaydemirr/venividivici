# TODO: Add questions by category endpoints
# TODO: Put upper limit on limit parameters
# TODO: Add await

from sanic import Sanic, text, Request, json, exceptions, file
from http import HTTPMethod

from worker.module import setup_modules
from worker.db_setup import setup_db

DEFAULT = (
    "blueprints.answers",
    "blueprints.categories",
    "blueprints.cities",
    "blueprints.countries",
    "blueprints.login",
    "blueprints.questions",
    "blueprints.replies",
    "blueprints.search",
    "blueprints.subscriptions",
    "blueprints.users",
    "blueprints.votes",
)

def create_app(parameters = None) -> Sanic:
    module_names = DEFAULT

    app = Sanic(name="venividivici")

    if not app.config.get("CORS-ORIGINS"):
        app.config.CORS_ORIGINS = "*"

    setup_db(app_name="venividivici", db_url="sqlite:///:memory:")
    setup_modules(app, *module_names)

    return app