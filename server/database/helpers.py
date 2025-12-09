from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from server.database.definitions import *
from sqlalchemy import func

class Database:
    def __init__(self, database_server_url: str):
        self.__engine = create_engine(database_server_url)
        self.__Session = sessionmaker(bind=self.__engine)
        self.__session = self.__Session()

    