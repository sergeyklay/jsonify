# This file is part of the Jsonify.
#
# (c) 2021 airSlate <support@airslate.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import os
from pathlib import Path

from dotenv import load_dotenv
from app import create_app

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=Path('.') / '.env')

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.route('/')
def index():
    return 'Hello, World!'
