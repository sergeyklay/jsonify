# This file is part of the Jsonify.
#
# (c) 2021 airSlate <support@airslate.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The main entry point for Jsonify."""

import inspect
import os

from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade

from app import create_app, db, models

dotenv_path = os.path.join(os.path.dirname(__file__), 'app.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)

app = create_app(os.getenv('FLASK_CONFIG', 'default'))
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """Configure flask shell command  to automatically import app objects."""
    return dict(
        app=app,
        db=db,
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
