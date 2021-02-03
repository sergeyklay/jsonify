# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from flask import request

from jsonify import logger
from jsonify.sdk.impl.resource_fields.parser import (
    Response,
    parse_request,
    create_request,
)
from . import api


@api.route('/resources/setup', methods=['POST'])
def resource_setup():
    """Resource fields URL"""
    contents = request.get_json()
    logger.info('Received resource payload %s' % contents)

    fields = parse_request(create_request(contents))
    response = Response(fields)

    logger.info('Return response %s' % response)

    return response
