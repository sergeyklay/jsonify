# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code

from app import db
from app.models import Organization
from app.sdk.generic.collections import path


def extract_id(data: dict) -> str or None:
    """Extract Organization ID from given dictionary."""
    return path(data, 'relationships.organization.data.id')


def connect(org: Organization) -> Organization:
    # TODO:
    # try:
    #     ...
    #     Log 'Organization connected.' + organization.serialize
    # catch:
    #     Log 'Error occurred during organization connection.'
    return org


def disconnect(org_id: int) -> bool:
    rows = db.session.query(Organization).filter_by(organization_uid=org_id).delete()
    db.session.commit()

    return bool(rows)
