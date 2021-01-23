# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from app.sdk.exceptions import ValidationError


Base = declarative_base()


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True)
    organization_uid = Column(String(32), nullable=False, unique=True)
    domain = Column(String(512), nullable=True)
    token = Column(Text, nullable=True)
    token_expires_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    @staticmethod
    def from_uid(uid):
        """A factory method to create Organization instance."""
        if not uid:
            raise ValidationError('Organization UID is required')

        return Organization(organization_uid=uid)

    @property
    def serialize(self) -> dict:
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'organization_uid': self.organization_uid,
            'domain': self.domain,
            'token': self.token,
            'token_expires_at': self.token_expires_at,
            'created_at': self.created_at,
        }

    def __repr__(self):
        """Returns the object representation in string format."""
        return '<Organization %r>' % self.organization_uid
