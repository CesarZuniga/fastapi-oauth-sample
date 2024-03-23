from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))


db_url = os.environ.get("DB_CONN")
engine: Engine = create_engine(db_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)