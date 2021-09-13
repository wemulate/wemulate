from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session
from wemulate.ext.settings.config import get_db_location
from sqlalchemy.orm import sessionmaker

database_engine: Engine = create_engine(
    f"sqlite+pysqlite:///{get_db_location()}", future=True
)
db_session: sessionmaker = sessionmaker(bind=database_engine, expire_on_commit=False)
