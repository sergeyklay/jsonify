# This file is part of the Jsonify.
#
# (c) 2021 airSlate <support@airslate.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The error handler module for the application.

Functions:

    access_denied(e) -> Any
    internal_server_error(e) -> Any
    page_not_found(e) -> Any
    request_wants_json() -> bool


"""

from flask import jsonify, render_template, request

from . import main


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


@main.app_errorhandler(403)
def access_denied(e):
    """Registers a function to handle 403 errors."""
    # Respond differently based on the MIME type accepted.
    if request_wants_json():
        # TODO(egrep): provide a template for error responses
        response = jsonify({'error': 'access denied'})
        response.status_code = 403
        return response
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    """Registers a function to handle 404 errors."""
    # Respond differently based on the MIME type accepted.
    if request_wants_json():
        # TODO(egrep): provide a template for error responses
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """Registers a function to handle 500 errors."""
    # Respond differently based on the MIME type accepted.
    if request_wants_json():
        # TODO(egrep): provide a template for error responses
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template('500.html'), 500
