from datetime import datetime

import pytest

from src.domain.entities import ChatContext, ChatMessage, Product


def build_product(**overrides) -> Product:
    data = {
        "id": 1,
        "name": "Nike Air Zoom",
        "brand": "Nike",
        "category": "Running",
        "size": "42",
        "color": "Negro",
        "price": 120.0,
        "stock": 5,
        "description": "Zapato para correr",
    }
    data.update(overrides)
    return Product(**data)


def build_message(**overrides) -> ChatMessage:
    data = {
        "id": 1,
        "session_id": "session-1",
        "role": "user",
        "message": "Hola",
        "timestamp": datetime(2026, 4, 22, 10, 0, 0),
    }
    data.update(overrides)
    return ChatMessage(**data)


def test_product_is_available_when_stock_is_positive() -> None:
    product = build_product(stock=3)

    assert product.is_available() is True


def test_product_reduce_stock_updates_remaining_units() -> None:
    product = build_product(stock=5)

    product.reduce_stock(2)

    assert product.stock == 3


def test_product_reduce_stock_raises_when_quantity_is_greater_than_stock() -> None:
    product = build_product(stock=2)

    with pytest.raises(ValueError, match="suficiente stock"):
        product.reduce_stock(3)


def test_product_validates_price_must_be_positive() -> None:
    with pytest.raises(ValueError, match="precio debe ser mayor a 0"):
        build_product(price=0)


def test_chat_message_validates_role() -> None:
    with pytest.raises(ValueError, match="rol debe ser"):
        build_message(role="system")


def test_chat_context_formats_recent_messages_for_prompt() -> None:
    messages = [
        build_message(id=1, role="user", message="Hola"),
        build_message(id=2, role="assistant", message="Te ayudo"),
    ]
    context = ChatContext(messages=messages, max_messages=2)

    formatted = context.format_for_prompt()

    assert formatted == "Usuario: Hola\nAsistente: Te ayudo"
