from typing import Callable
from functools import wraps

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from wemulate.core.exc import WEmulateDatabaseError, WEmulateValidationError
from wemulate.core.database.session import init_database_session, database_engine
from wemulate.core.database.models import init_database


def use_db_session(method: Callable) -> Callable:
    @wraps(method)
    def inner(*method_args, **method_kwargs) -> None:
        init_database(database_engine)
        db_session = init_database_session()
        try:
            with db_session.begin() as session:
                return_value = method(session, *method_args, **method_kwargs)
            return return_value
        except IntegrityError as e:
            splitting = e.args[0].split(
                "(sqlite3.IntegrityError) UNIQUE constraint failed: connection.", 1
            )[1]
            raise WEmulateValidationError(message=splitting)
        except SQLAlchemyError as e:
            raise WEmulateDatabaseError(e.args[0])

    return inner
