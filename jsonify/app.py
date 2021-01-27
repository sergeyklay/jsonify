# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Manage the application creation and configuration process.

Functions:

    create_app(config: str) -> flask.Flask
    load_env_vars(base_path: str) -> None
    configure_app(app: Flask, config_name=None) -> None
    configure_blueprints(app: Flask) -> None
    configure_extensions(app: Flask) -> None

"""

import os

from flask import Flask


def create_app(config=None) -> Flask:
    """Creates the application."""
    app = Flask(__name__)

    configure_app(app, config)
    configure_blueprints(app)
    configure_extensions(app)

    return app


def load_env_vars(base_path: str):
    """Load the current dotenv as system environment variable."""
    dotenv_path = os.path.join(base_path, '.env')

    from dotenv import load_dotenv
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)


def configure_app(app: Flask, config_name=None):
    """Configure Jsonify application."""
    from jsonify.config import config, Config

    # Use the default config and override it afterwards
    app.config.from_object(config['default'])

    if config is not None:
        # Config name as a string
        if isinstance(config_name, str) and config_name in config:
            app.config.from_object(config[config_name])
            config[config_name].init_app(app)
        # Config as an object
        else:
            app.config.from_object(config_name)
            if isinstance(config_name, Config):
                config_name.init_app(app)

    # Update config from environment variable (if any).
    # Export this variable as follows:
    #   export JSONIFY_SETTINGS="/var/www/server/config.py"
    app.config.from_envvar('JSONIFY_SETTINGS', silent=True)


def configure_blueprints(app: Flask):
    """Configure blueprints for the application."""
    # main blueprint registration
    from jsonify.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # api blueprint registration
    from jsonify.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')


def configure_extensions(app: Flask):
    """Configure extensions for the application."""
    from jsonify.models import db

    # Flask-SQLAlchemy
    db.init_app(app)
