"""
Modelos ORM para la base de datos.

Define las tablas y sus relaciones utilizando SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from src.infrastructure.db.database import Base


class ProductModel(Base):
    """
    Modelo ORM para la tabla de productos.
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    category = Column(String, nullable=False)
    size = Column(String, nullable=False)
    color = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    description = Column(String, nullable=False)


class ChatMessageModel(Base):
    """
    Modelo ORM para la tabla de mensajes del chat.
    """

    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    role = Column(String, nullable=False)  # user / assistant
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    