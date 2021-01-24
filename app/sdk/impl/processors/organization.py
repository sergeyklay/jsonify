# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from flask import current_app
from requests.exceptions import RequestException
from sqlalchemy import exc

from app import db
from app import logger
from app.models import Organization
from app.sdk.exceptions import InternalServerError
from app.sdk.exceptions import OrganizationConnect, OrganizationDisconnect
from app.sdk.impl.authenticator import authenticate


def connect(organization: Organization) -> Organization:
    try:
        client_id = current_app.config.get('BOT_CLIENT_ID')
        client_secret = current_app.config.get('BOT_CLIENT_SECRET')

        identity = authenticate(
            organization.organization_uid,
            client_id,
            client_secret
        )

        organization.token = identity.token
        organization.domain = identity.domain
        organization.token_expires_at = identity.expires

        db.session.add(organization)
        db.session.flush()
    except exc.IntegrityError as integrity_error:
        logger.error(integrity_error)

        db.session.rollback()
        raise OrganizationConnect(
            message='Already connected',
            payload={'detail': 'Requested organization already connected.'}
        )
    except (exc.SQLAlchemyError, RequestException) as internal_error:
        logger.error(internal_error)

        db.session.rollback()
        raise InternalServerError(
            payload={'detail': 'Unable to connect organization.'}
        )
    else:
        db.session.commit()
        logger.info(
            'Organization %s successfully connected' %
            organization.organization_uid
        )

        return organization


def disconnect(org_uid: str):
    rows = db.session.query(Organization).filter_by(organization_uid=org_uid).delete()
    db.session.commit()

    status = bool(rows)
    if not status:
        raise OrganizationDisconnect(
            status_code=404,
            message='Not Found',
            payload={'detail': 'Requested organization does not exist.'}
        )

    logger.info(
        'Organization %s successfully disconnected' %
        org_uid
    )
