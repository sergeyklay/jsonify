# This file is part of the Jsonify.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

def test_root_entrypoint(client):
    """Go to the root an see welcome."""
    rv = client.get('/')
    assert b'JSON pre-fill add-on.' in rv.data


def test_not_found(client):
    """See error when page not found."""
    rv = client.get('/foo/bar')
    expected = {
        'errors': [
            {
                'status': '404',
                'title':  'Page Not Found',
            }
        ]
    }

    assert expected == rv.json
    assert rv.status_code == 404
