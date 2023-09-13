from werkzeug.exceptions import HTTPException


class NotFoundError(HTTPException):
    code = 404

    def __init__(self, description):
        self.description = description


class BadRequest(HTTPException):
    def __init__(self, description):
        self.description = description
        self.code = 400


class RequestEntityTooLarge(HTTPException):
    code = 413

    def __init__(self, description):
        self.description = description


class Notimplemented(HTTPException):
    code = 501

    def __init__(self, description):
        self.description = description


class InternalServerError(HTTPException):
    code = 500

    def __init__(self, description):
        self.description = description












