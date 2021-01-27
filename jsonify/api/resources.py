# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from flask import request

from jsonify.api import api
from jsonify.sdk.impl.http.views.resources import handle_setup


@api.route('/resources/setup', methods=['POST'])
def resource_setup():
    """Resource fields URL"""
    content = request.get_json()
    return handle_setup(content)
