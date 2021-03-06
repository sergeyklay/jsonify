# This file is part of the Jsonify.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Standard exception hierarchy for Jsonify."""

from http import HTTPStatus


class ApiError(Exception):
    status_code = HTTPStatus.BAD_REQUEST.value

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        if isinstance(self.message, dict):
            errors = []
            for message in self.message:
                error = dict(())
                # JSON API specification says that status member of Error
                # Object should be expressed as string value.
                error['status'] = str(self.status_code)
                error['title'] = message
                errors.append(error)
        else:
            error = dict(self.payload or ())
            # JSON API specification says that status member of Error
            # Object should be expressed as string value.
            error['status'] = str(self.status_code)
            error['title'] = self.message
            errors = [error]

        return {'errors': errors}


class InternalServerError(ApiError):
    def __init__(self, message=None, payload=None):
        if not message:
            message = HTTPStatus.INTERNAL_SERVER_ERROR.phrase

        super().__init__(
            message=message,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            payload=payload
        )


class BadRequest(ApiError):
    def __init__(self, message, payload=None):
        super().__init__(
            message=message,
            payload=payload,
            status_code=400
        )


class ValidationError(BadRequest):
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
