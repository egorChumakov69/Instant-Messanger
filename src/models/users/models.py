from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=32), unique=True, index=True)
    password = Column(String(length=128), nullable=False)
    first_name = Column(String(length=64), nullable=True)
    last_name = Column(String(length=64), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    telegram_id = Column(BigInteger, nullable=True)
    telegram_link_token = Column(String(length=12), nullable=True)
    telegram_chat_id = Column(BigInteger, nullable=True)

    sent_messages = relationship('Message', back_populates='sender', foreign_keys='Message.sender_id')
    received_messages = relationship('Message', back_populates='receiver', foreign_keys='Message.receiver_id')
    refresh_token = relationship('RefreshToken', back_populates='user', cascade='all, delete-orphan')
