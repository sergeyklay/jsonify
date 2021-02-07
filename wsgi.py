# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The main entry point for Jsonify."""

import os

from addon.app import create_app, load_env_vars

load_env_vars(os.path.dirname(os.path.abspath(__file__)))

app = create_app(os.getenv('JSONIFY_CONFIG', 'default'))
