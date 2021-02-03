# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from jsonify import logger
from jsonify.sdk.impl.resource_fields.parser import Request, Response, parse_request


def handle_setup(payload):
    logger.info('Received resource payload %s' % payload)

    request = Request.from_dict(payload)
    fields = parse_request(request)
    response = Response(fields)

    logger.info('Return response %s' % response)

    return response
