# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from . import api


@api.route('/prefill/resource/fields', methods=['POST'])
def prefill_fields():
    raise NotImplementedError()


@api.route('/organization/connect', methods=['POST'])
def organization_connect():
    raise NotImplementedError()


@api.route('/prefill/handle/event', methods=['POST'])
def handle_event():
    raise NotImplementedError()
