# This file is part of the Jsonify.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.


import codecs
from os import path
from setuptools import setup, find_packages
import re


def locate_package_directory():
    """Identify a directory of the package and its associated files."""
    try:
        return path.abspath(path.dirname(__file__))
    except Exception as path_error:
        message = ('The directory in which the package and its '
                   'associated files are stored could not be located.')
        raise RuntimeError(message) from path_error


def read_file(filepath):
    """Read content from a UTF-8 encoded text file."""
    with codecs.open(filepath, 'rb', 'utf-8') as file_handle:
        return file_handle.read()


PKG_NAME = 'jsonify'
PKG_DIR = locate_package_directory()
META_PATH = path.join(PKG_DIR, 'bot', '__init__.py')
META_CONTENTS = read_file(META_PATH)


def load_long_description():
    """Load long description from file README.rst."""
    def changes():
        changelog = path.join(PKG_DIR, 'CHANGELOG.rst')
        pat = r"(\d+.\d.\d \(.*?\)\r?\n.*?)\r?\n\r?\n\r?\n----\r?\n\r?\n\r?\n"
        result = re.search(pat, read_file(changelog), re.S)

        if result:
            return result.group(1)
        else:
            return ''

    try:
        read_me = path.join(PKG_DIR, 'README.rst')
        authors = path.join(PKG_DIR, 'AUTHORS.rst')

        title = f"{PKG_NAME}: {find_meta('description')}\n"
        head = '=' * len(title) + '\n'

        contents = (
                head
                + format(title.strip(' .'))
                + head
                + read_file(read_me).split('.. teaser-begin')[1]
                + "\n\n"
                + "Release Information\n"
                + "===================\n\n"
                + changes()
                + "\n\n`Full changelog "
                + f"<{find_meta('url')}/blob/master/CHANGELOG.rst>`_.\n\n"
                + read_file(authors)
        )

        return contents
    except Exception as read_error:
        message = 'Long description could not be read from README.rst'
        raise RuntimeError(message) from read_error


def is_canonical_version(version):
    """Check if a version string is in the canonical format of PEP 440."""
    pattern = (
        r'^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))'
        r'*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))'
        r'?(\.dev(0|[1-9][0-9]*))?$')
    return re.match(pattern, version) is not None


def find_meta(meta):
    """Extract __*meta*__ from META_CONTENTS."""
    meta_match = re.search(
        r"^__{meta}__\s+=\s+['\"]([^'\"]*)['\"]".format(meta=meta),
        META_CONTENTS,
        re.M
    )

    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(
        f'Unable to find __{meta}__ string in package meta file')


def get_version_string():
    """Return package version as listed in `__version__` in meta file."""
    # Parse version string
    version_string = find_meta('version')

    # Check validity
    if not is_canonical_version(version_string):
        message = (
            'The detected version string "{}" is not in canonical '
            'format as defined in PEP 440.'.format(version_string))
        raise ValueError(message)

    return version_string


KEYWORDS = [
    'airslate',
    'crm',
    'nocode',
    'addons',
    'bots',
]

# Classifiers: available ones listed at https://pypi.org/classifiers
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Natural Language :: English',

    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',

    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3 :: Only',
]

# Dependencies that are downloaded by pip on installation and why
INSTALL_REQUIRES = [
    'airslate>=0.2.1,==0.*',  # Interact with airSlate HTTP API
    'asdicts>=1.1.0,==1.*',  # Utilities for working with Python dictionaries
    'flask>=1.1.2,==1.1.*',  # Our framework
    'flask-migrate>=2.6.0,==2.*',  # Wrapper for alembic
    'flask-sqlalchemy>=2.4.4,==2.*',  # Wrapper for sqlalchemy
    'python-dotenv>=0.15.0,==0.*',  # Read the key-value pair from .env file

]

# List additional groups of dependencies here (e.g. testing dependencies).
# You can install these using the following syntax, for example:
#
#    $ pip install -e .[develop,testing]
#
EXTRAS_REQUIRE = {
    # Dependencies that are required to run tests
    'testing': [
        'pytest>=6.2.2',  # Our tests framework
        'pytest-cov>=2.11.1',  # Pytest plugin for measuring coverage
    ],
}

# Project's URLs
PROJECT_URLS = {
    'Bug Tracker': 'https://github.com/sergeyklay/jsonify/issues',
    'Source Code': 'https://github.com/sergeyklay/jsonify',
}

if __name__ == '__main__':
    setup(
        name=PKG_NAME,
        version=get_version_string(),
        author=find_meta('author'),
        author_email=find_meta('author_email'),
        maintainer=find_meta('author'),
        maintainer_email=find_meta('author_email'),
        license=find_meta('license'),
        description=find_meta('description'),
        long_description=load_long_description(),
        long_description_content_type='text/x-rst',
        keywords=KEYWORDS,
        url=find_meta('url'),
        project_urls=PROJECT_URLS,
        classifiers=CLASSIFIERS,
        packages=find_packages(),
        platforms='any',
        include_package_data=True,
        zip_safe=False,
        python_requires='>=3.7, <4',
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
    )
