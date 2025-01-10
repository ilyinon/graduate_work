from models.promocodes import IdMixin, ModelBase, TimestampMixin
from sqlalchemy import Column, String


class User(ModelBase, TimestampMixin, IdMixin):
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), unique=True)
