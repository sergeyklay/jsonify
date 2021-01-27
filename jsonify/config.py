# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    JSONIFY_CLIENT_ID = os.getenv('JSONIFY_CLIENT_ID')
    JSONIFY_CLIENT_SECRET = os.getenv('JSONIFY_CLIENT_SECRET')
    API_BASE_URI = os.getenv('API_BASE_URI', 'https://api.airslate.com')
    BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DEV_DATABASE_URL',
        'sqlite:///' + os.path.join(Config.BASE_PATH, 'db-dev.sqlite3')
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URL',
        'sqlite://'  # in-memory
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(Config.BASE_PATH, 'db.sqlite3')
    )


class DockerConfig(ProductionConfig):
    @staticmethod
    def init_app(app):
        super().init_app(app)

        from logging import StreamHandler
        stream_handler = StreamHandler()
        stream_handler.setLevel('INFO')
        app.logger.addHandler(stream_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,

    'default': DevelopmentConfig,
}
