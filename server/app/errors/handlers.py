from flask import request
from app.errors import bp
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)
def not_found_error(error):
    return error_response(404)



@bp.app_errorhandler(500)
def internal_error(error):
    return error_response(500)




def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    return error_response(400, message)