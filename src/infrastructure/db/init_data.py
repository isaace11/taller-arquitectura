"""
Carga de datos iniciales para la aplicación.

Este módulo inserta productos de ejemplo en la base de datos
si la tabla de productos se encuentra vacía.
"""

from src.infrastructure.db.database import SessionLocal
from src.infrastructure.db.models import ProductModel


def load_initial_data() -> None:
    """
    Carga productos iniciales si no existen registros previos.

    Returns:
        None
    """
    db = SessionLocal()

    try:
        existing_products = db.query(ProductModel).count()

        if existing_products > 0:
            return

        products = [
            ProductModel(
                name="Nike Air Zoom Pegasus",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=120.0,
                stock=5,
                description="Zapato de running con excelente amortiguación.",
            ),
            ProductModel(
                name="Adidas Ultraboost 21",
                brand="Adidas",
                category="Running",
                size="41",
                color="Blanco",
                price=150.0,
                stock=3,
                description="Modelo cómodo y ligero para correr largas distancias.",
            ),
            ProductModel(
                name="Puma Suede Classic",
                brand="Puma",
                category="Casual",
                size="40",
                color="Azul",
                price=80.0,
                stock=10,
                description="Zapato casual clásico para uso diario.",
            ),
            ProductModel(
                name="Nike Revolution 6",
                brand="Nike",
                category="Running",
                size="43",
                color="Gris",
                price=95.0,
                stock=7,
                description="Opción versátil para entrenamiento y running.",
            ),
            ProductModel(
                name="Adidas Grand Court",
                brand="Adidas",
                category="Casual",
                size="42",
                color="Blanco",
                price=85.0,
                stock=6,
                description="Estilo clásico inspirado en tenis.",
            ),
            ProductModel(
                name="Puma RS-X",
                brand="Puma",
                category="Casual",
                size="41",
                color="Negro",
                price=110.0,
                stock=4,
                description="Diseño moderno con gran comodidad.",
            ),
            ProductModel(
                name="Nike Air Max SC",
                brand="Nike",
                category="Casual",
                size="44",
                color="Blanco",
                price=130.0,
                stock=5,
                description="Modelo urbano con cámara de aire visible.",
            ),
            ProductModel(
                name="Adidas Duramo SL",
                brand="Adidas",
                category="Running",
                size="40",
                color="Rosado",
                price=90.0,
                stock=8,
                description="Zapato ligero ideal para trote y gimnasio.",
            ),
            ProductModel(
                name="Puma Smash v2",
                brand="Puma",
                category="Casual",
                size="39",
                color="Blanco",
                price=75.0,
                stock=9,
                description="Modelo casual con estilo minimalista.",
            ),
            ProductModel(
                name="Nike Downshifter 12",
                brand="Nike",
                category="Running",
                size="41",
                color="Azul",
                price=105.0,
                stock=6,
                description="Zapato de running con soporte y ligereza.",
            ),
        ]

        db.add_all(products)
        db.commit()
    finally:
        db.close()
        