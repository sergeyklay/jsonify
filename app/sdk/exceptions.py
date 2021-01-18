# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from http import HTTPStatus


class ApiError(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['status'] = self.status_code
        rv['title'] = self.message
        return rv


class ValidationError(ApiError):
    def __init__(self, message, status_code=None, payload=None):
        super(ValidationError, self).__init__(message, status_code, payload)


class InvalidUsage(ApiError):
    def __init__(self, message, status_code=None, payload=None):
        super(InvalidUsage, self).__init__(message, status_code, payload)


class OrganizationAbsent(ApiError):
    def __init__(self, payload=None):
        super(OrganizationAbsent, self).__init__(
            'Organization is not found.',
            HTTPStatus.NOT_FOUND,
            payload
        )


class OrganizationPresent(ApiError):
    def __init__(self, payload=None):
        super(OrganizationPresent, self).__init__(
            message='Integrity failure, organization in use.',
            payload=payload
        )
