from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from wemulate.utils.helper import get_db_location
from sqlalchemy.orm import sessionmaker

database_engine: Engine = create_engine(
    f"sqlite+pysqlite:///{get_db_location()}", future=True
)
Session = sessionmaker(bind=database_engine)
session = Session()
