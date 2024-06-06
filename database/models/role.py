from app import db
from enum import Enum
from sqlalchemy.types import EnumType

class RoleType(Enum):
    writer = 'writer'
    producer = 'producer'
    director = 'director'
    actor = 'actor'

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(EnumType(RoleType), unique=True, nullable=False)