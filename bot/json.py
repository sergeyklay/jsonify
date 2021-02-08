# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import json
import os
from urllib.error import HTTPError
from urllib.request import urlopen, Request

from asdicts.dict import path

from .client import create_client
from .exceptions import ValidationError, BadRequest


def create_storage(settings, org_id):
    if 'json_url' in settings:
        return JsonUrlStorage(settings['json_url'])

    if 'attachment' in settings:
        return JsonFileStorage(path(settings, 'attachment.file_id'), org_id)

    raise ValidationError('Invalid storage settings')


class JsonUrlStorage:
    def __init__(self, url):
        self.url = url

    @property
    def contents(self):
        try:
            user_agent = os.environ.get('CRAWLER_USER_AGENT')
            timeout = int(os.environ.get('CRAWLER_TIMEOUT', 5))

            if not user_agent:
                headers = {}
            else:
                headers = {'User-Agent': user_agent}

            request = Request(self.url, headers=headers)
            with urlopen(request, timeout=timeout) as response:
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
    def __init__(self, file_id, org_id):
        self.file_id = file_id
        self.org_id = org_id

    @property
    def contents(self):
        client = create_client(self.org_id)
        stream = client.slate_addon_files.download(self.file_id)

        file_contents = ''

        # With the following streaming code, the Python memory usage is
        # restricted regardless of the size of the downloaded file:
        with stream as r:
            for chunk in r.iter_content(chunk_size=512, decode_unicode=True):
                file_contents += chunk

        return file_contents


class JsonDecoder:

    def __init__(self, contents):
        self.contents = json.loads(contents)

    def list_paths(self):
        """Create paths of all nested dictionary values.

        >>> my_dict = {'a': [1, 2], 'b': 42, 'c': {'c1': 17, 'c2': [1, 2, 3]}}
        >>> my_result = self.list_paths()
        >>> print(my_result)
        ['a', 'c.c2']
        """
        result = []
        paths = self._find_list_fields(self.contents)

        for p in map(lambda x: '.'.join(x), paths):
            result.append(p)

        return result

    def fields(self, the_path):
        """Get self.contents[the_path] dictionary keys as a list.

        >>> my_dict = {'a': {'a1', 1, 'a2': 2}}
        >>> my_result = self.fields('a')
        >>> print(my_result)
        ['a1', 'a2']
        """
        result = []
        first_object = path(self.contents, the_path)
        if isinstance(first_object, list) and len(first_object):
            first_object = first_object[0]
        if isinstance(first_object, dict):
            result = first_object.keys()
        return result

    def _find_list_fields(self, obj, container=None):
        """Create paths of all nested dictionary values.

        >>> my_dict = {'a': [1, 2], 'b': 42, 'c': {'c1': 17, 'c2': [1, 2, 3]}}
        >>> result = self._find_list_fields(my_dict)
        >>> print(list(result))
        [['a'], ['c', 'c2']]
        """
        if container is None:
            container = []

        for k, v in obj.items():
            new_container = container + [k]
            if isinstance(v, dict):
                for u in self._find_list_fields(v, new_container):
                    yield u
            elif isinstance(v, list):
                yield new_container
