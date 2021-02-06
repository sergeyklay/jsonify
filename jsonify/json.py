# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import json
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from jsonify.exceptions import ValidationError, BadRequest

SETTING_JSON_URL = 'json_url'
SETTING_ATTACHMENT = 'attachment'

FETCH_CONTENTS_TIMEOUT = 5  # 5 seconds max

CRAWLER_USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) ' +
                      'AppleWebKit/605.1.15 (KHTML, like Gecko) ' +
                      'Version/14.0.3 Safari/605.1.15')


def create_storage(settings, org_id):
    if SETTING_JSON_URL in settings:
        return JsonUrlStorage(settings[SETTING_JSON_URL])

    if SETTING_ATTACHMENT in settings:
        return JsonFileStorage()

    raise ValidationError('Invalid storage settings')


class JsonUrlStorage:
    def __init__(self, url):
        self.url = url

    @property
    def contents(self):
        try:
            headers = {'User-Agent': CRAWLER_USER_AGENT}
            request = Request(self.url, headers=headers)
            with urlopen(request, timeout=FETCH_CONTENTS_TIMEOUT) as response:
                contents = response.read().decode('utf-8')

            return contents
        except HTTPError as exc_info:
            msg = str(exc_info)
            raise BadRequest(
                message='Unable to fetch JSON contents from the remote server',
                payload={
                    'detail': f'Response from the remote server: {msg}: {self.url}'
                }
            )


class JsonFileStorage:
    @property
    def contents(self):
        return {}


class JsonDecoder:

    def __init__(self, contents):
        self.contents = json.loads(contents)

    def list_paths(self):
        """Create paths of all nested dictionary values.

        >>> my_dict = {'a': [1, 2], 'b': 42, 'c': {'c1': 17, 'c2': [1, 2, 3]}}
        >>> my_result = self.list_paths(my_dict)
        >>> print(list(my_result))
        ['a', 'c.c2']
        """
        result = []
        paths = self.find_list_fields(self.contents)

        for p in map(lambda x: '.'.join(x), paths):
            result.append(p)

        return result

    def find_list_fields(self, obj, path=None):
        """Create paths of all nested dictionary values.

        >>> my_dict = {'a': [1, 2], 'b': 42, 'c': {'c1': 17, 'c2': [1, 2, 3]}}
        >>> result = self.find_list_fields(my_dict)
        >>> print(list(result))
        [['a'], ['c', 'c2']]
        """
        if path is None:
            path = []

        for k, v in obj.items():
            new_path = path + [k]
            if isinstance(v, dict):
                for u in self.find_list_fields(v, new_path):
                    yield u
            elif isinstance(v, list):
                yield new_path
