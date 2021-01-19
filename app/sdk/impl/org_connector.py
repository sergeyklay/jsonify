# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code

from sqlalchemy import exc

from app import db
from app.models import Organization
from app.sdk.exceptions import OrganizationConnect


def connect(organization: Organization) -> Organization:
    try:
        db.session.add(organization)
        db.session.flush()
    except exc.IntegrityError:
        db.session.rollback()
        raise OrganizationConnect(payload={'id': organization.organization_uid})
    else:
        db.session.commit()
        return organization


def disconnect(org_uid: str) -> bool:
    rows = db.session.query(Organization).filter_by(organization_uid=org_uid).delete()
    db.session.commit()

    return bool(rows)
