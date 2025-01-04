from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import EmailStr
from sqlalchemy import Column, ForeignKey, String

ModelBase = declarative_base()


class IdMixin(object):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.now())
    modified_at = Column(DateTime, onupdate=datetime.now(), default=datetime.now())


class Promocodes(ModelBase, IdMixin, TimestampMixin):
    __tablename__ = "promocodes"

    promocode = Column(String, unique=True, index=True)
    discount_percent = Column(Float, default=0.0)  # Скидка в процентах
    discount_rubles = Column(Float, default=0.0)    # Фиксированная скидка в валюте
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    usage_limit = Column(Integer, nullable=True, default=0)   # Максимальное количество использований
    used_count = Column(Integer, default=0)        # Текущее количество использований
    is_active = Column(Boolean, default=True)
    is_one_time = Column(Boolean, default=True)    # Одноразовый или многоразовый