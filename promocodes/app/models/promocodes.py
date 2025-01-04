from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PromoCode(Base):
    __tablename__ = "promocodes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    discount_percent = Column(Float, default=0.0)  # Скидка в процентах
    fixed_discount = Column(Float, default=0.0)    # Фиксированная скидка в валюте
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    usage_limit = Column(Integer, nullable=True)   # Максимальное количество использований
    used_count = Column(Integer, default=0)        # Текущее количество использований
    is_active = Column(Boolean, default=True)
    is_one_time = Column(Boolean, default=True)    # Одноразовый или многоразовый