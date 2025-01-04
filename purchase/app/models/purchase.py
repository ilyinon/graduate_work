from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()








class IdMixin(object):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


class TimestampMixin(object):
    created = Column(DateTime, default=datetime.now())
    modified = Column(DateTime, onupdate=datetime.now(), default=datetime.now())


class User(Base, IdMixin):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    purchases = relationship("Purchase", back_populates="user")

class Tariff(Base, IdMixin, TimestampMixin):
    __tablename__ = "tariffs"

    name = Column(String)
    description = Column(String)
    price = Column(Float)

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
