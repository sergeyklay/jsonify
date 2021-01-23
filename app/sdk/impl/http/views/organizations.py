# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from http import HTTPStatus

from app import logger
from app.models import Organization
from app.sdk.collections import path
from app.sdk.exceptions import BadRequest, ValidationError
from app.sdk.impl.org_extractor import extract_id
from app.sdk.impl.processors.organization import connect, disconnect


def handle_connection(payload):
    if not payload or not isinstance(payload, dict):
        raise BadRequest('No input data provided')

    data = payload.get('data')
    if not data or not isinstance(data, dict):
        raise BadRequest('Invalid payload, missed "data"')

    should_disconnect = path(payload, 'meta.disconnected') or False

    org_uid = extract_id(data)
    if not org_uid:
        raise ValidationError('Organization id is missed')

    logger.info(
        'Received %s webhook for organization %s' %
        (('disconnect' if should_disconnect else 'connect'), org_uid)
    )

    if should_disconnect:
        disconnect(org_uid)
        message = 'Organization disconnected.'
    else:
        connect(Organization.from_uid(org_uid))
        message = 'Organization connected.'

    response = {'message': f'{message}'}
    return response, HTTPStatus.OK
