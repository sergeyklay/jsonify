# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from collections.abc import Sequence
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
        if isinstance(self.message, Sequence) and \
                not isinstance(self.message, (str, bytes, bytearray)):
            errors = []
            for message in self.message:
                error = dict(())
                error['status'] = self.status_code
                error['title'] = message
                errors.append(error)
        else:
            error = dict(self.payload or ())
            error['status'] = self.status_code
            error['title'] = self.message
            errors = [error]

        return {'errors': errors}


class InternalServerError(ApiError):
    def __init__(self, message=None, payload=None):
        if not message:
            message = 'Internal Server Error.'

        super().__init__(
            message=message,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            payload=payload
        )


class ValidationError(ApiError):
    def __init__(self, message, payload=None):
        super().__init__(
            message=message,
            payload=payload
        )


class InvalidUsage(ApiError):
    def __init__(self, message, payload=None):
        super().__init__(
            message=message,
            payload=payload
        )


class OrganizationConnect(ApiError):
    def __init__(self, message=None, status_code=None, payload=None):
        if not message:
            message = 'Error occurred during organization connect process.'

        super().__init__(
            message=message,
            status_code=status_code,
            payload=payload
        )


class OrganizationDisconnect(ApiError):
    def __init__(self, message=None, status_code=None, payload=None):
        if not message:
            message = 'Error occurred during organization disconnect process.'

        super().__init__(
            message=message,
            status_code=status_code,
            payload=payload
        )
