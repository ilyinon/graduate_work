from models.base import ModelBase
from models.mixin import IdMixin, TimestampMixin
from models.base import ModelBase
from sqlalchemy import Column, ForeignKey, String, Float, Boolean, Integer
from sqlalchemy import Column, DateTime


class Promocodes(ModelBase, IdMixin, TimestampMixin):
    __tablename__ = "promocodes"

    promocode = Column(String, unique=True, index=True)
    discount_percent = Column(Float, default=0.0)
    discount_rubles = Column(Float, default=0.0)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    usage_limit = Column(Integer, nullable=True, default=0)
    used_count = Column(Integer, nullable=True, default=0)
    is_active = Column(Boolean, default=True)
    is_one_time = Column(Boolean, default=True)
