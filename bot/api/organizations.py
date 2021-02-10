# This file is part of the Jsonify.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from http import HTTPStatus

from asdicts.dict import path
from flask import request

from bot import logger
from bot.api import api
from bot.exceptions import BadRequest, ValidationError
from bot.models import Organization
from bot.processors.organization import connect, disconnect


@api.route('/organizations/connect', methods=['POST'])
def handle_connection():
    """Handle bot connections.

    Gets notifications when the bot is added to a flow in an
    organization for the firs time.
    """
    contents = request.get_json()

    if not isinstance(contents, dict):
        raise BadRequest('No input data provided')

    data = contents.get('data')
    if not data or not isinstance(data, dict):
        raise BadRequest('Invalid payload, missed "data"')

    should_disconnect = path(contents, 'meta.disconnected') or False

    org_uid = path(data, 'relationships.organization.data.id')
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
        connect(Organization.from_id(org_uid))
        message = 'Organization connected.'

    response = {'message': f'{message}'}
    return response, HTTPStatus.OK
