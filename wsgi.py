# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The main entry point for Jsonify."""

import inspect
import os

from flask_migrate import Migrate, upgrade
from jsonify import create_app, load_env_vars, models

_basepath = os.path.dirname(os.path.abspath(__file__))

load_env_vars(_basepath)

app = create_app(os.getenv('JSONIFY_CONFIG', 'default'))
migrate = Migrate(app, models.db)


@app.shell_context_processor
def make_shell_context():
    """Configure flask shell command  to automatically import app objects."""
    return dict(
        app=app,
        db=models.db,
        **dict(inspect.getmembers(models, inspect.isclass)))


@app.cli.command()
def test():
    """Run the unit test."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # Migrate database to latest revision.
    upgrade()
