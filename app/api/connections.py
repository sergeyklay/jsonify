# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from http import HTTPStatus

from flask import request

from app.api import api
from app.models import Organization
from app.sdk.impl.organization import extract_id, connect


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

    org_id = extract_id(data)
    if not org_id:
        response = {'message': 'Invalid payload, missed organization id'}
        return response, HTTPStatus.BAD_REQUEST

    organization = connect(Organization(organization_uid=org_id))
    # db.session.add(organization)
    # db.session.commit()

    response = {'message': 'Organization connected.'}
    return response, HTTPStatus.OK
