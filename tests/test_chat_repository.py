from datetime import datetime, timedelta

from src.domain.entities import ChatMessage
from src.infrastructure.repositories.chat_repository import SQLChatRepository


def build_message(
    session_id: str,
    role: str,
    message: str,
    offset_seconds: int,
) -> ChatMessage:
    return ChatMessage(
        id=None,
        session_id=session_id,
        role=role,
        message=message,
        timestamp=datetime(2026, 4, 22, 10, 0, 0) + timedelta(seconds=offset_seconds),
    )


def test_save_message_persists_chat_message(db_session) -> None:
    repository = SQLChatRepository(db_session)
    message = build_message("user123", "user", "Hola", 0)

    saved_message = repository.save_message(message)

    assert saved_message.id is not None
    assert saved_message.session_id == "user123"


def test_get_session_history_returns_messages_in_chronological_order(db_session) -> None:
    repository = SQLChatRepository(db_session)
    repository.save_message(build_message("user123", "user", "Hola", 0))
    repository.save_message(build_message("user123", "assistant", "Te ayudo", 1))

    history = repository.get_session_history("user123")

    assert len(history) == 2
    assert history[0].message == "Hola"
    assert history[1].message == "Te ayudo"


def test_get_session_history_respects_limit(db_session) -> None:
    repository = SQLChatRepository(db_session)
    repository.save_message(build_message("user123", "user", "Uno", 0))
    repository.save_message(build_message("user123", "assistant", "Dos", 1))
    repository.save_message(build_message("user123", "user", "Tres", 2))

    history = repository.get_session_history("user123", limit=2)

    assert len(history) == 2
    assert history[0].message == "Dos"
    assert history[1].message == "Tres"


def test_get_recent_messages_returns_last_messages_in_order(db_session) -> None:
    repository = SQLChatRepository(db_session)
    repository.save_message(build_message("user123", "user", "Uno", 0))
    repository.save_message(build_message("user123", "assistant", "Dos", 1))
    repository.save_message(build_message("user123", "user", "Tres", 2))

    recent_messages = repository.get_recent_messages("user123", 2)

    assert len(recent_messages) == 2
    assert recent_messages[0].message == "Dos"
    assert recent_messages[1].message == "Tres"


def test_delete_session_history_returns_deleted_count(db_session) -> None:
    repository = SQLChatRepository(db_session)
    repository.save_message(build_message("user123", "user", "Hola", 0))
    repository.save_message(build_message("user123", "assistant", "Te ayudo", 1))

    deleted_count = repository.delete_session_history("user123")

    assert deleted_count == 2
    assert repository.get_session_history("user123") == []
