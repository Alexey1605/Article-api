import json

from flask import Response
from marshmallow import ValidationError
from webargs.flaskparser import parser
from werkzeug.exceptions import HTTPException


def _make_error_body(code, name, description=None, **kwargs):
    body = {
        'code': code,
        'name': name
    }
    if description:
        body['description'] = description
    body |= kwargs
    return body


def handle_exceptions(e):
    content_type = 'application/json'

    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = json.dumps(_make_error_body(e.code, e.name, e.description))
        response.content_type = content_type
        return response

    elif isinstance(e, ValidationError):
        body = _make_error_body(400, 'Bad request', e.messages)
        return Response(json.dumps(body), status=400, mimetype=content_type)


@parser.error_handler
def handle_request_parsing_error(error, req, schema, *, error_status_code, error_headers):
    """
    This error handler is necessary for usage with Flask -
    webargs error handler that return a JSON error response to the client.
    """
    raise error
