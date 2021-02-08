# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from .exceptions import ValidationError

db = SQLAlchemy()


class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    organization_uid = db.Column(db.String(32), nullable=False, unique=True)
    domain = db.Column(db.String(512), nullable=True)
    token = db.Column(db.Text, nullable=True)
    token_expires_at = db.Column(db.TIMESTAMP, nullable=True)

    @staticmethod
    def from_id(uid):
        """A factory method to create Organization instance."""
        if not uid:
            raise ValidationError('Organization UID is required')

        return Organization(organization_uid=uid)

    def token_expired(self) -> bool:
        """Check if token is expired."""
        sec = int((self.token_expires_at - datetime.utcnow()).total_seconds())
        return sec <= 1

    def token_valid(self) -> bool:
        return self.token is not None and not self.token_expired()

    def __repr__(self):
        """Returns the object representation in string format."""
        return '<Organization %r>' % self.organization_uid
