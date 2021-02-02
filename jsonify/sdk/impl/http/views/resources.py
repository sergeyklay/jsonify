# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from jsonify.sdk.impl.resource_fields import Parser, Request, Response


def handle_setup(payload):
    request = Request.from_dict(payload)
    parser = Parser()

    fields = parser.parse(request)
    response = Response(fields)

    return response
