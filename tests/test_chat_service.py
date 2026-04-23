import asyncio
from datetime import datetime

import pytest

from src.application.chat_service import ChatService
from src.application.dtos import ChatMessageRequestDTO
from src.domain.entities import ChatMessage, Product
from src.domain.exceptions import ChatServiceError
from src.domain.repositories import IChatRepository, IProductRepository


class FakeProductRepository(IProductRepository):
    def __init__(self) -> None:
        self.products = [
            Product(
                id=1,
                name="Nike Air",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=120,
                stock=5,
                description="Zapato para correr",
            )
        ]

    def get_all(self):
        return self.products

    def get_by_id(self, product_id):
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def get_by_brand(self, brand):
        return [product for product in self.products if product.brand == brand]

    def get_by_category(self, category):
        return [product for product in self.products if product.category == category]

    def save(self, product):
        return product

    def delete(self, product_id):
        return True


class FakeChatRepository(IChatRepository):
    def __init__(self) -> None:
        self.messages = []

    def save_message(self, message):
        saved_message = ChatMessage(
            id=len(self.messages) + 1,
            session_id=message.session_id,
            role=message.role,
            message=message.message,
            timestamp=message.timestamp,
        )
        self.messages.append(saved_message)
        return saved_message

    def get_session_history(self, session_id, limit=None):
        history = [message for message in self.messages if message.session_id == session_id]
        if limit is not None:
            history = history[-limit:]
        return history

    def delete_session_history(self, session_id):
        original_count = len(self.messages)
        self.messages = [message for message in self.messages if message.session_id != session_id]
        return original_count - len(self.messages)

    def get_recent_messages(self, session_id, count):
        history = [message for message in self.messages if message.session_id == session_id]
        return history[-count:]


class FakeAIService:
    async def generate_response(self, user_message, products, context):
        return f"Respuesta simulada para: {user_message}"


class FailingAIService:
    async def generate_response(self, user_message, products, context):
        raise RuntimeError("Fallo del proveedor")


@pytest.fixture
def chat_dependencies():
    product_repo = FakeProductRepository()
    chat_repo = FakeChatRepository()
    return product_repo, chat_repo


def test_process_message_saves_user_and_assistant_messages(chat_dependencies) -> None:
    product_repo, chat_repo = chat_dependencies
    service = ChatService(product_repo, chat_repo, FakeAIService())
    request = ChatMessageRequestDTO(
        session_id="user123",
        message="Hola, busco zapatos para correr",
    )

    response = asyncio.run(service.process_message(request))

    assert response.session_id == "user123"
    assert "Respuesta simulada" in response.assistant_message
    assert len(chat_repo.messages) == 2
    assert chat_repo.messages[0].role == "user"
    assert chat_repo.messages[1].role == "assistant"


def test_get_session_history_returns_messages_as_dtos(chat_dependencies) -> None:
    product_repo, chat_repo = chat_dependencies
    chat_repo.messages = [
        ChatMessage(
            id=1,
            session_id="user123",
            role="user",
            message="Hola",
            timestamp=datetime(2026, 4, 22, 10, 0, 0),
        ),
        ChatMessage(
            id=2,
            session_id="user123",
            role="assistant",
            message="Te ayudo",
            timestamp=datetime(2026, 4, 22, 10, 0, 1),
        ),
    ]
    service = ChatService(product_repo, chat_repo, FakeAIService())

    history = service.get_session_history("user123")

    assert len(history) == 2
    assert history[0].role == "user"
    assert history[1].role == "assistant"


def test_clear_session_history_returns_deleted_count(chat_dependencies) -> None:
    product_repo, chat_repo = chat_dependencies
    chat_repo.messages = [
        ChatMessage(
            id=1,
            session_id="user123",
            role="user",
            message="Hola",
            timestamp=datetime(2026, 4, 22, 10, 0, 0),
        ),
        ChatMessage(
            id=2,
            session_id="user123",
            role="assistant",
            message="Te ayudo",
            timestamp=datetime(2026, 4, 22, 10, 0, 1),
        ),
    ]
    service = ChatService(product_repo, chat_repo, FakeAIService())

    deleted_count = service.clear_session_history("user123")

    assert deleted_count == 2
    assert chat_repo.messages == []


def test_process_message_wraps_provider_errors(chat_dependencies) -> None:
    product_repo, chat_repo = chat_dependencies
    service = ChatService(product_repo, chat_repo, FailingAIService())
    request = ChatMessageRequestDTO(
        session_id="user123",
        message="Hola, busco zapatos para correr",
    )

    with pytest.raises(ChatServiceError, match="Error al procesar el mensaje del chat"):
        asyncio.run(service.process_message(request))
