from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class IdMixin(object):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


class TimestampMixin(object):
    created = Column(DateTime, default=datetime.now())
    modified = Column(DateTime, onupdate=datetime.now(), default=datetime.now())


from models.base import ModelBase
from models.mixin import IdMixin, TimestampMixin
from pydantic import EmailStr
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash


class User(ModelBase, TimestampMixin, IdMixin):
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), unique=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))


class Tariff(Base, IdMixin, TimestampMixin):
    __tablename__ = "tariffs"

    name = Column(String)
    description = Column(String)
    price = Column(Float, nullable=False)


class Purchase(Base, IdMixin, TimestampMixin):
    __tablename__ = "purchases"

    user_id = Column(Integer, ForeignKey("users.id"))
    tariff_id = Column(Integer, ForeignKey("tariffs.id"))
    amount = Column(Float)
    is_successful = Column(Boolean, default=False)
    failure_reason = Column(String, nullable=True)
    promocode_code = Column(String, nullable=True)

    user = relationship("User", back_populates="purchases")
    tariff = relationship("Tariff")
