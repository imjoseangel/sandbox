# -*- coding: utf-8 -*-

from datetime import datetime
from config import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Naming(db.Model):
    __tablename__ = "resourceDefinition"
    index = db.Column(db.Integer)
    name = db.Column(db.String(64), primary_key=True,
                     unique=True, nullable=False)
    regex = db.Column(db.String(256))
    scope = db.Column(db.String(16))
    slug = db.Column(db.String(16))
    dashes = db.Column(db.Boolean())
    lengthmin = db.Column(db.Integer())
    lengthmax = db.Column(db.Integer())


class NamingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Naming
        include_fk = True
        include_relationships = True
        load_instance = True
