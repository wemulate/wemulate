from typing import Callable
from wemulate.core.exc import WEmulateDatabaseError, WEmulateValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from functools import wraps
from wemulate.core.database.session import db_session


def use_db_session(method: Callable) -> Callable:
    @wraps(method)
    def inner(*method_args, **method_kwargs) -> None:
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
