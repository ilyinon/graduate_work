from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

ModelBase = declarative_base()


class IdMixin(object):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.now())
    modified_at = Column(DateTime, onupdate=datetime.now(), default=datetime.now())


class User(ModelBase, TimestampMixin, IdMixin):
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), unique=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))

    user_tariff = relationship("UserTariff", back_populates="user", lazy="selectin")
    purchase = relationship("Purchase", back_populates="user", lazy="selectin")


class Tariff(ModelBase, IdMixin, TimestampMixin):
    __tablename__ = "tariffs"

    name = Column(String)
    description = Column(String)
    price = Column(Float, nullable=False)

    purchase = relationship("Purchase", back_populates="tariff")
    user_tariff = relationship(
        "UserTariff", back_populates="tariff"
    )

class UserTariff(ModelBase, IdMixin, TimestampMixin):
    __tablename__ = "user_tariff"
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    tariff_id = Column(
        UUID(as_uuid=True), ForeignKey("tariffs.id", ondelete="CASCADE"), nullable=False
    )

    tariff = relationship("Tariff", back_populates="user_tariff", lazy="selectin")
    user = relationship("User", back_populates="user_tariff", lazy="selectin")


class Purchase(ModelBase, IdMixin, TimestampMixin):
    __tablename__ = "purchases"

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    tariff_id = Column(
        UUID(as_uuid=True), ForeignKey("tariffs.id", ondelete="CASCADE"), nullable=False
    )
    amount = Column(Float)
    is_successful = Column(Boolean, default=False)
    failure_reason = Column(String, nullable=True)
    promocode_code = Column(String, nullable=True)

    tariff = relationship("Tariff", back_populates="purchase", lazy="selectin")
    user = relationship("User", back_populates="purchase", lazy="selectin")
