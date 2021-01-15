# This file is part of the Jsonify.
#
# (c) 2021 airSlate <support@airslate.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

load_dotenv(dotenv_path=Path('.') / '.env')

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'
