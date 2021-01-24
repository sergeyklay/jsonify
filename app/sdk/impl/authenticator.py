# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code

import time
from dataclasses import dataclass
from datetime import datetime

from airslate.client import Client
from flask import current_app
from app import logger
from app.sdk.collections import path
from app.sdk.exceptions import BadRequest


@dataclass
class AddonIdentity:
    """Class for storing addon identity."""
    token: str
    domain: str
    expires: datetime


def authenticate(org_uid: str, client_id: str, client_secret: str) -> AddonIdentity:
    client = Client(base_url=current_app.config.get('API_BASE_URI'))

    logger.info(
        'Trying to authenticate bot %s for organization %s' %
        (client_id, org_uid)
    )

    # We're expect a response in the following format:
    #    {
    #        'meta': {
    #            'token_type': 'Bearer',
    #            'expires': 1209000,
    #            'access_token': '...',
    #            'refresh_token': '...',
    #            'domain': '',
    #        }
    #    }
    #
    identity = client.addons.access_token(org_uid, client_id, client_secret)

    logger.info(
        'Received identity webhook for organization %s: %s' %
        (org_uid, identity)
    )

    if 'meta' not in identity:
        raise BadRequest(message='The `meta` field is required.')

    token = path(identity, 'meta.access_token')
    domain = path(identity, 'meta.domain')
    expires = path(identity, 'meta.expires')

    if expires and token and domain:
        expires = datetime.fromtimestamp(
            int(time.time()) + int(expires)
        )

        return AddonIdentity(token, domain, expires)

    fields = {'expires': expires, 'access_token': token, 'domain': domain}
    missed = [k for k in fields.keys() if not fields[k]]
    message = map(lambda f: f'The `meta.{f}` field is required.', missed)

    raise BadRequest(message=list(message))
