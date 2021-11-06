# -*- coding: utf-8 -*-

from datetime import datetime
from config import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Naming(db.Model):
    __tablename__ = "resourceDefinition"
    resource_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    length = db.Column(db.String(32))
    regex = db.Column(db.String(256))
    scope = db.Column(db.String(16))
    slug = db.Column(db.String(16))
    dashes = db.Column(db.Boolean())
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class NamingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Naming
        include_fk = True
        include_relationships = True
        load_instance = True
