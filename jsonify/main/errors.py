# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The error handler module for the application.

Functions:

    handle_api_error(e) -> Any
    bad_request(e) -> Any
    access_denied(e) -> Any
    page_not_found(e) -> Any
    internal_server_error(e) -> Any
    service_unavailable(e) -> Any


"""

from flask import jsonify

from jsonify.exceptions import ApiError
from jsonify.main import main


@main.app_errorhandler(ApiError)
def handle_api_error(error):
    errors = error.to_dict()
    response = jsonify(errors)
    response.status_code = error.status_code
    return response


@main.app_errorhandler(400)
def bad_request(e):
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
def service_unavailable(e):
    """Registers a function to handle 503 errors."""
    return handle_api_error(ApiError('Service Temporarily Unavailable', 503))
