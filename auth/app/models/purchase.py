from sqlalchemy import Boolean, Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.base import ModelBase
from models.mixin import IdMixin, TimestampMixin


class Tariff(ModelBase, IdMixin, TimestampMixin):
    __tablename__ = "tariffs"

    name = Column(String)
    description = Column(String)
    price = Column(Float, nullable=False)


class UserTariff(ModelBase, IdMixin, TimestampMixin):
    __tablename__ = "user_tariff"
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    tariff_id = Column(
        UUID(as_uuid=True), ForeignKey("tariffs.id", ondelete="CASCADE"), nullable=False
    )

    tariff = relationship("Tariff", back_populates="tariff", lazy="selectin")
    user = relationship("User", back_populates="roles", lazy="selectin")


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

    tariff = relationship("Tariff", back_populates="tariff", lazy="selectin")
    user = relationship("User", back_populates="roles", lazy="selectin")
