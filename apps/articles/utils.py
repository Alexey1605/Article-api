from flask import Response


def create_response(data: str = None, status_code: int = 200):
    return Response(data, status_code, mimetype='application/json')