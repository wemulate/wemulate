import os
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from wemulate.ext.settings.config import get_db_location

if os.environ.get("WEMULATE_TESTING"):
    database_engine: Engine = create_engine("sqlite:///:memory:")
else:
    database_engine: Engine = create_engine(
        f"sqlite+pysqlite:///{get_db_location()}", future=True
    )


def init_database_session() -> sessionmaker:
    return sessionmaker(bind=database_engine, expire_on_commit=False)
