"""
Configuración de la base de datos.

Este módulo establece la conexión con SQLite utilizando SQLAlchemy
y proporciona la sesión de base de datos para el resto de la aplicación.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import settings

# Motor de base de datos
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # Necesario para SQLite
)

# Sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base para modelos ORM
Base = declarative_base()


def get_db():
    """
    Generador de sesiones de base de datos.

    Yields:
        Session: Sesión activa de la base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        