from models.base import ModelBase
from models.mixin import IdMixin, TimestampMixin
from models.base import ModelBase
from sqlalchemy import Column, ForeignKey, String, Float, Boolean, Integer
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


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


    user_promocodes = relationship("UserPromocodes", back_populates="promocode")


class UserPromocodes(ModelBase, IdMixin, TimestampMixin):
    __tablename__ = "user_promocodes"

    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    promocode_id = Column(UUID, ForeignKey('promocodes.id'), nullable=False)

    user = relationship("Users", back_populates="user_promocodes")
    promocode = relationship("Promocodes", back_populates="user_promocodes")