# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The top-level module for the application.

This module tracks the version of the application as well as the
base application info used by various functions within the
package and provides a factory function to create application
instance.

Functions:

    create_app(config: str) -> flask.Flask
    load_env_vars(base_path: str) -> None

Misc variables:

    __author__
    __author_email__
    __copyright__
    __description__
    __license__
    __url__
    __version__
    logger

"""

from flask import current_app
from werkzeug.local import LocalProxy
from jsonify.app import load_env_vars, create_app

# TODO: Move outside or use builtin logger
logger = LocalProxy(lambda: current_app.logger)

__copyright__ = 'Copyright (c) 2021 airSlate, Inc.'
__version__ = '1.0.0a1'
__license__ = 'Apache 2.0'
__author__ = 'Serghei Iakovlev'
__author_email__ = 'i.serghei@pdffiller.com'
__url__ = 'https://github.com/sergeyklay/as-jsonify-bot'
__description__ = 'Example bot for developers.airslate.com'
