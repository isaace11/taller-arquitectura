"""
Inicialización de la base de datos.

Este script crea las tablas definidas en los modelos ORM
y carga datos iniciales si la base está vacía.
"""

from src.infrastructure.db.database import engine, Base
from src.infrastructure.db import models
from src.infrastructure.db.init_data import load_initial_data


def init_db() -> None:
    """
    Inicializa la base de datos y carga datos iniciales.

    Returns:
        None
    """
    Base.metadata.create_all(bind=engine)
    load_initial_data()


if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada correctamente.")
    