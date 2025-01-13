from datetime import datetime
from uuid import uuid4

from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        Null, String)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

ModelBase = declarative_base()


class IdMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.now())
    modified_at = Column(DateTime, onupdate=datetime.now(), default=datetime.now())


class Promocodes(ModelBase, IdMixin, TimestampMixin):
    __tablename__ = "promocodes"

    promocode = Column(String, unique=True, index=True)
    discount_percent = Column(Float, default=0.0)
    discount_rubles = Column(Float, default=0.0)
    start_date = Column(DateTime(timezone=True), nullable=True, default=datetime.now())
    end_date = Column(DateTime(timezone=True), nullable=True, default=Null)
    usage_limit = Column(Integer, nullable=True, default=0)
    used_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, nullable=False)
    is_one_time = Column(Boolean, default=True, nullable=False)

    user_promocodes = relationship("UserPromocodes", back_populates="promocode")


class UserPromocodes(ModelBase, IdMixin, TimestampMixin):
    __tablename__ = "user_promocodes"

    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    promocode_id = Column(UUID, ForeignKey("promocodes.id"), nullable=False)

    user = relationship("User", back_populates="user_promocodes")
    promocode = relationship("Promocodes", back_populates="user_promocodes")
