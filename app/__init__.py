# This file is part of the Jsonify.
#
# (c) 2021 airSlate <support@airslate.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The top-level module for Jsonify.

This module tracks the version of the package as well as the base
package info used by various functions within Jsonify and provides
a factory function to create application instance.

Functions:

    create_app(config_name: str) -> flask.Flask

Misc variables:

    __copyright__
    __version__
    __license__
    __author__
    __author_email__
    __url__
    __description__

"""

from flask import Flask

from config import config

__copyright__ = 'Copyright (C) 2021 airSlate'
__version__ = '1.0.0.alpha1'
__license__ = 'Apache 2.0'
__author__ = 'Serghei Iakovlev'
__author_email__ = 'i.serghei@pdffiller.com'
__url__ = 'https://github.com/sergeyklay/as-jsonify-bot'
__description__ = 'Example bot for developers.airslate.com'


def create_app(config_name: str) -> Flask:
    """Factory function to create application instance."""
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    return app
