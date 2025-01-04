from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    is_successful = Column(Boolean, default=False)
    promocode_id = Column(Integer, ForeignKey("promocodes.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    failure_reason = Column(String, nullable=True)

    user = relationship("User", back_populates="purchases")
    promocode = relationship("PromoCode")
