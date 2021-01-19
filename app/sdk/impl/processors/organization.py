# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from sqlalchemy import exc

from app import db
from app.models import Organization
from app.sdk.exceptions import OrganizationConnect
from app.sdk.exceptions import OrganizationDisconnect


def connect(organization: Organization) -> Organization:
    try:
        db.session.add(organization)
        db.session.flush()
    except exc.IntegrityError:
        # TODO:
        # message = 'Error occurred during organization connection.' + exc
        # logger.error(message)

        db.session.rollback()
        raise OrganizationConnect(payload={'id': organization.organization_uid})
    else:
        db.session.commit()
        # TODO:
        # message = 'Organization connected.'
        # logger.info(message)

        return organization


def disconnect(org_uid: str):
    rows = db.session.query(Organization).filter_by(organization_uid=org_uid).delete()
    db.session.commit()

    status = bool(rows)
    if not status:
        raise OrganizationDisconnect(payload={'id': org_uid})

    # TODO:
    # message = 'Disconnecting organization.' + org_uid
