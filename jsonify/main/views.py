# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The routes module for the application."""

import os
from distutils.util import strtobool

from flask import abort

from . import main


@main.before_app_request
def maintained():
    try:
        maintenance = strtobool(os.getenv('JSONIFY_MAINTENANCE', 'False'))
        if bool(maintenance):
            abort(503)
    except ValueError:
        pass


@main.route('/405')
def not_allowed():
    abort(405)


@main.route('/')
def index():
    return 'JSON pre-fill add-on.'
