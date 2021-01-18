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
from app.sdk.generic.collections import path
from app.sdk.impl.organization import extract_id, connect, disconnect


@api.route('/organization/connect', methods=['POST'])
def organization_connect():
    content = request.get_json()  # type: dict
    if not content:
        response = {'message': 'No input data provided'}
        return response, HTTPStatus.BAD_REQUEST

    data = content.get('data')  # type: dict
    if not data:
        response = {'message': 'Invalid payload, missed "data"'}
        return response, HTTPStatus.BAD_REQUEST

    should_disconnect = path(content, 'meta.disconnected') or False
    current_app.logger.info(
        'Received %s webhook' %
        ('disconnect' if should_disconnect else 'connect')
    )

    org_id = extract_id(data)
    if not org_id:
        response = {'message': 'Invalid payload, missed organization id'}
        return response, HTTPStatus.BAD_REQUEST

    if should_disconnect:
        status = disconnect(org_id)
        if status:
            message = 'Organization disconnected.'
            response = {'message': 'Organization disconnected.'}
            current_app.logger.info(message)  # TODO: + org_id

            return response, HTTPStatus.OK
        else:
            response = {'message': f'Organization with uid {org_id} is not found.'}
            return response, HTTPStatus.BAD_REQUEST
    else:
        org = Organization.from_uid(org_id)
        # TODO: Get access token and domain for org_id

        # TODO: Add access token and domain to Organization
        organization = connect(org)

        # TODO: Save to database
        try:
            db.session.add(organization)
            db.session.flush()
        except exc.IntegrityError as error:
            db.session.rollback()

            existing = db.session \
                .query(Organization) \
                .filter_by(organization_uid=org_id) \
                .one()

            message = f'Integrity failure, organization in use: {existing}'
            response = {'message': message}

            current_app.logger.error(message)  # TODO: + error
            return response, HTTPStatus.BAD_REQUEST
        else:
            db.session.commit()

            message = 'Organization connected'
            current_app.logger.info(message)
            response = {'message': f'{message}.'}

            return response, HTTPStatus.OK
