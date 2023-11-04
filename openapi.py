from flask import send_from_directory


def openapi():
    return send_from_directory('../../docs', 'openapi.json')
