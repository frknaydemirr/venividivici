from sanic import Sanic

from database.crud import Database 
from database.external_api_helpers import External_API_Helpers
from database.models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

def setup_db(app_name: str, db_url: str) -> None:
    app = Sanic.get_app(app_name)

    @app.before_server_start
    async def setup(app, loop) -> None:
        engine = create_engine(db_url)
        session = Session(engine)

        ext = External_API_Helpers(session)

        Base.metadata.create_all(engine)

        if ext.check_if_database_is_empty():
            ext.insert_all_countries()
            ext.insert_all_cities()

        app.ctx.db = Database(session)
        app.ctx.session = session