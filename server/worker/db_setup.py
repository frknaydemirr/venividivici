from sanic import Sanic

from server.database.crud import Database 
from server.database.external_api_helpers import External_API_Helpers
from server.database.models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def setup_db(app_name: str, db_url: str, external_session = None) -> None:
    app = Sanic.get_app(app_name)

    if external_session:
        @app.before_server_start
        async def setup_external(app, loop) -> None:
            app.ctx.db = Database(external_session)

        return

    def _new_engine_session():
        engine = create_engine(db_url, pool_size=20)
        return engine, Session(engine)

    @app.main_process_start
    async def prepare_schema(app, loop) -> None:
        engine, session = _new_engine_session()

        try:
            Base.metadata.create_all(engine, checkfirst=True)

            ext = External_API_Helpers(session)
            if ext.check_if_database_is_empty():
                ext.insert_all_countries()
                ext.insert_all_cities()
        finally:
            session.close()
            engine.dispose()

    @app.before_server_start
    async def setup_worker(app, loop) -> None:
        engine, session = _new_engine_session()
        app.ctx.db_engine = engine
        app.ctx.db_session = session
        app.ctx.db = Database(session)

    @app.after_server_stop
    async def shutdown_worker(app, loop) -> None:
        session = getattr(app.ctx, "db_session", None)
        if session:
            session.close()

        engine = getattr(app.ctx, "db_engine", None)
        if engine:
            engine.dispose()