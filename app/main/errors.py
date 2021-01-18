# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The error handler module for the application.

Functions:

    handle_api_error(e) -> Any
    access_denied(e) -> Any
    internal_server_error(e) -> Any
    page_not_found(e) -> Any
    request_wants_json() -> bool


"""

from flask import jsonify, render_template, request

from app.main import main
from app.sdk.exceptions import ApiError


def request_wants_json() -> bool:
    """Check if client wants a JSON response."""
    json_types = [
        'application/vnd.api+json',
        'application/json',
    ]

    html_type = 'text/html'
    accept_types = json_types + [html_type]
    best = request.accept_mimetypes.best_match(accept_types)

    # Some clients accept on '*/*' and we don't want to
    # deliver JSON to an ordinary browser.
    return (best in json_types) and \
        request.accept_mimetypes[best] > request.accept_mimetypes[html_type]


@main.app_errorhandler(ApiError)
def handle_api_error(error):
    if request_wants_json():
        errors = {'errors': [error.to_dict()]}
        response = jsonify(errors)
        response.status_code = error.status_code
        return response

    return render_template(
        'http_error.html',
        message=error.message,
        status_code=error.status_code,
    ), error.status_code


@main.app_errorhandler(400)
def access_denied(e):
    """Registers a function to handle 400 errors."""
    return handle_api_error(ApiError('Bad Request', 400))


@main.app_errorhandler(403)
def access_denied(e):
    """Registers a function to handle 403 errors."""
    return handle_api_error(ApiError('Access Denied', 403))


@main.app_errorhandler(404)
def page_not_found(e):
    """Registers a function to handle 404 errors."""
    return handle_api_error(ApiError('Page Not Found', 404))


@main.app_errorhandler(500)
def internal_server_error(e):
    """Registers a function to handle 500 errors."""
    return handle_api_error(ApiError('Internal Server Error', 500))


@main.app_errorhandler(503)
def internal_server_error(e):
    """Registers a function to handle 503 errors."""
    return handle_api_error(ApiError('Service Temporarily Unavailable', 503))
