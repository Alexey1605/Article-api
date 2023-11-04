from functools import wraps

from flask import Response
from apps.core.extensions import db


def create_response(data: str = None, status_code: int = 200):
    return Response(data, status_code, mimetype='application/json')


def provide_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not kwargs.get('session'):
            kwargs['session'] = db.session()
        return func(*args, **kwargs)
    return wrapper
