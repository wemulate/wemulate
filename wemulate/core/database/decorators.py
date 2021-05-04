from typing import Callable
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
from wemulate.core.database.session import session

def rollback_if_necessary(method: Callable) -> Callable:
    @wraps(method)
    def inner(*method_args, **method_kwargs) -> None:
        try:
            method(*method_args, **method_kwargs)
        except SQLAlchemyError:
            session.rollback()
    return inner
