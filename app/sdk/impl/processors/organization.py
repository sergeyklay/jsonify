# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from app.models import Organization
from app.sdk.exceptions import ApiError
from app.sdk.exceptions import OrganizationDisconnect
from app.sdk.impl import org_connector


def connect(organization: Organization) -> Organization:
    try:
        org_connector.connect(organization)

        # TODO:
        # message = 'Organization connected.'
        # logger.info(message)

        return organization
    except ApiError as api_error:
        # TODO:
        # message = 'Error occurred during organization connection.' + exc
        # logger.error(message)

        raise api_error


def disconnect(org_uid: str):
    # TODO:
    # message = 'Disconnecting organization.' + org_uid
    status = org_connector.disconnect(org_uid)
    if not status:
        raise OrganizationDisconnect(payload={'id': org_uid})
