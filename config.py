# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    APP_SLOW_DB_QUERY_TIME = 0.5
    BOT_CLIENT_ID = os.getenv('BOT_CLIENT_ID')
    BOT_CLIENT_SECRET = os.getenv('BOT_CLIENT_SECRET')
    API_BASE_URI = os.getenv('API_BASE_URI', 'https://api.airslate.com')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DEV_DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'db-dev.sqlite3')
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
        'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    )


class DockerConfig(ProductionConfig):
    @staticmethod
    def init_app(app):
        from logging import StreamHandler
        log_handler = StreamHandler()
        log_handler.setLevel('INFO')
        app.logger.addHandler(log_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,

    'default': DevelopmentConfig,
}
