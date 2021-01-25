# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

from app.sdk.exceptions import ValidationError

db = SQLAlchemy()


class Organization(declarative_base()):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True)
    organization_uid = Column(String(32), nullable=False, unique=True)
    domain = Column(String(512), nullable=True)
    token = Column(Text, nullable=True)
    token_expires_at = Column(TIMESTAMP, nullable=True)

    @staticmethod
    def from_uid(uid):
        """A factory method to create Organization instance."""
        if not uid:
            raise ValidationError('Organization UID is required')

        return Organization(organization_uid=uid)

    def token_expired(self) -> bool:
        """Check if token is expired."""
        return (self.token_expires_at - datetime.utcnow()).total_seconds() > 0

    def token_valid(self) -> bool:
        return self.token is not None and not self.token_expired()

    def __repr__(self):
        """Returns the object representation in string format."""
        return '<Organization %r>' % self.organization_uid
