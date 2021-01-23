# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from flask import request

from app.api import api
from app.sdk.impl.http.views.organizations import handle_connection


@api.route('/organizations/connect', methods=['POST'])
def organization_connect():
    """Connect organization URL."""
    content = request.get_json()
    return handle_connection(content)