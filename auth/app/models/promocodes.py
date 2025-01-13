from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.base import ModelBase
from models.mixin import IdMixin, TimestampMixin


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

    user_to_promocodes = relationship("UserPromocodes", back_populates="promocodes")


class UserPromocode(ModelBase, IdMixin, TimestampMixin):
    __tablename__ = "user_promocodes"

    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    promocode_id = Column(UUID, ForeignKey("promocodes.id"), nullable=False)

    user = relationship("User", back_populates="user_promocodes", lazy="selectin")
    promocodes = relationship(
        "Promocodes", back_populates="user_to_promocodes", lazy="selectin"
    )
