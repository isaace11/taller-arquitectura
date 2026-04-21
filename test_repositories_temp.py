from datetime import datetime

from src.infrastructure.db.database import SessionLocal
from src.infrastructure.repositories.product_repository import SQLProductRepository
from src.infrastructure.repositories.chat_repository import SQLChatRepository
from src.domain.entities import Product, ChatMessage


def test_product_repository():
    db = SessionLocal()
    repo = SQLProductRepository(db)

    print("=== PRODUCT REPOSITORY ===")

    # Crear producto
    product = Product(
        id=None,
        name="Adidas Run",
        brand="Adidas",
        category="Running",
        size="41",
        color="Azul",
        price=100,
        stock=10,
        description="Zapato deportivo",
    )

    saved = repo.save(product)
    print("CREADO:", saved)

    # Obtener todos
    all_products = repo.get_all()
    print("TODOS:", all_products)

    # Obtener por ID
    found = repo.get_by_id(saved.id)
    print("POR ID:", found)

    # Eliminar
    deleted = repo.delete(saved.id)
    print("ELIMINADO:", deleted)

    db.close()


def test_chat_repository():
    db = SessionLocal()
    repo = SQLChatRepository(db)

    print("\n=== CHAT REPOSITORY ===")

    # Crear mensajes
    msg1 = ChatMessage(
        id=None,
        session_id="test123",
        role="user",
        message="Hola",
        timestamp=datetime.utcnow(),
    )

    msg2 = ChatMessage(
        id=None,
        session_id="test123",
        role="assistant",
        message="Hola, ¿en qué puedo ayudarte?",
        timestamp=datetime.utcnow(),
    )

    repo.save_message(msg1)
    repo.save_message(msg2)

    # Obtener historial
    history = repo.get_session_history("test123")
    print("HISTORIAL:", history)

    # Obtener recientes
    recent = repo.get_recent_messages("test123", 1)
    print("RECIENTE:", recent)

    # Eliminar historial
    deleted = repo.delete_session_history("test123")
    print("ELIMINADOS:", deleted)

    db.close()


if __name__ == "__main__":
    test_product_repository()
    test_chat_repository()
    