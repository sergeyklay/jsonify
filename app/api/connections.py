# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from http import HTTPStatus

from flask import request, current_app
from sqlalchemy import exc

from app import db
from app.api import api
from app.models import Organization
from app.sdk import exceptions
from app.sdk.generic.collections import path
from app.sdk.impl.organization import extract_id, connect, disconnect


@api.route('/organization/connect', methods=['POST'])
def organization_connect():
    content = request.get_json()
    if not content:
        raise exceptions.InvalidUsage('No input data provided')

    data = content.get('data')
    if not data:
        raise exceptions.InvalidUsage('Invalid payload, missed "data"')

    should_disconnect = path(content, 'meta.disconnected') or False
    current_app.logger.info(
        'Received %s webhook' %
        ('disconnect' if should_disconnect else 'connect')
    )

    org_id = extract_id(data)
    if not org_id:
        raise exceptions.ValidationError('Organization UID is required')

    if should_disconnect:
        status = disconnect(org_id)
        if not status:
            raise exceptions.OrganizationAbsent({'uid': org_id})

        message = 'Organization disconnected.'
        response = {'message': 'Organization disconnected.'}
        current_app.logger.info(message)  # TODO: + org_id

        return response, HTTPStatus.OK
    else:
        org = Organization.from_uid(org_id)
        # TODO: Get access token and domain for org_id

        # TODO: Add access token and domain to Organization
        organization = connect(org)

        # TODO: Save to database
        try:
            db.session.add(organization)
            db.session.flush()
        except exc.IntegrityError:
            db.session.rollback()

            message = f'Integrity failure, organization {org_id} in use'
            current_app.logger.error(message)

            raise exceptions.OrganizationPresent({'uid': org_id})
        else:
            db.session.commit()

            message = 'Organization connected'
            current_app.logger.info(message)
            response = {'message': f'{message}.'}

            return response, HTTPStatus.OK
