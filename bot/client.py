# This file is part of the Jsonify.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from airslate.client import Client
from flask import current_app
from sqlalchemy.orm.exc import NoResultFound

from . import logger
from .models import Organization, db
from .processors.organization import connect


def create_client(org_id=None) -> Client:
    """Create :class:`Client` instance."""
    if org_id is None:
        return Client(base_url=current_app.config.get('API_BASE_URI'))

    config = _prepare_config(org_id)
    return Client(base_url=current_app.config.get('API_BASE_URI'), **config)


def _prepare_config(org_id: str):
    """Prepare configuration for :class:`Client` instance."""
    query = db.session.query(Organization).filter_by(organization_uid=org_id)

    try:
        organization = query.one()

        if not organization.token_valid():
            connect(organization)
    except NoResultFound:
        logger.info('Connecting new organization')
        organization = connect(Organization.from_id(org_id))

    return {
        'token': organization.token,
        'headers': {
            'Organization-Id': organization.organization_uid,
            'User-Agent': current_app.config.get('BOT_USER_AGENT'),
        }
    }
