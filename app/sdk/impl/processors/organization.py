# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from flask import current_app
from sqlalchemy import exc

from app import db
from app.models import Organization
from app.sdk.exceptions import InternalServerError
from app.sdk.exceptions import OrganizationConnect, OrganizationDisconnect
from app.sdk.impl.authenticator import authenticate
from requests.exceptions import RequestException


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
    except exc.IntegrityError:
        # TODO:
        # message = 'Error occurred during organization connection.' + exc
        # logger.error(message)

        db.session.rollback()
        raise OrganizationConnect(
            message='Already connected.',
            payload={
                'detail': 'Organization with UID {} already connected.'.format(
                    organization.organization_uid
                )
            }
        )
    except (exc.SQLAlchemyError, RequestException):
        # TODO:
        # message = 'Error occurred during organization connection.' + exc
        # logger.error(message)

        db.session.rollback()
        raise InternalServerError(
            payload={
                'detail': 'Unable to connect organization with UID {}.'.format(
                    organization.organization_uid
                )
            }
        )
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
        raise OrganizationDisconnect(
            status_code=404,
            message='Not Found.',
            payload={
                'detail': 'Organization with UID {} does not exist.'.format(
                    org_uid
                )
            }
        )

    # TODO:
    # message = 'Disconnecting organization.' + org_uid
