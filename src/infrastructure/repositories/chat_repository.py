"""
Repositorio de historial de chat usando SQLAlchemy.

Implementa el contrato definido en la capa de dominio
para gestionar mensajes del chat en la base de datos.
"""

from sqlalchemy.orm import Session

from src.domain.entities import ChatMessage
from src.domain.repositories import IChatRepository
from src.infrastructure.db.models import ChatMessageModel


class SQLChatRepository(IChatRepository):
    """
    Implementación concreta del repositorio de chat.

    Attributes:
        db (Session): Sesión activa de base de datos.
    """

    def __init__(self, db: Session) -> None:
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db (Session): Sesión SQLAlchemy.
        """
        self.db = db

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje en la base de datos.

        Args:
            message (ChatMessage): Mensaje a guardar.

        Returns:
            ChatMessage: Mensaje guardado con ID asignado.
        """
        message_model = self._entity_to_model(message)
        self.db.add(message_model)
        self.db.commit()
        self.db.refresh(message_model)
        return self._model_to_entity(message_model)

    def get_session_history(self, session_id: str, limit: int | None = None) -> list[ChatMessage]:
        """
        Obtiene el historial de una sesión en orden cronológico.

        Args:
            session_id (str): Identificador de la sesión.
            limit (int | None): Límite de mensajes.

        Returns:
            list[ChatMessage]: Historial de mensajes.
        """
        query = (
            self.db.query(ChatMessageModel)
            .filter(ChatMessageModel.session_id == session_id)
            .order_by(ChatMessageModel.timestamp.asc())
        )

        if limit is not None:
            messages = query.all()[-limit:]
        else:
            messages = query.all()

        return [self._model_to_entity(message) for message in messages]

    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todos los mensajes de una sesión.

        Args:
            session_id (str): Identificador de la sesión.

        Returns:
            int: Cantidad de mensajes eliminados.
        """
        messages = self.db.query(ChatMessageModel).filter(
            ChatMessageModel.session_id == session_id
        ).all()

        deleted_count = len(messages)

        for message in messages:
            self.db.delete(message)

        self.db.commit()
        return deleted_count

    def get_recent_messages(self, session_id: str, count: int) -> list[ChatMessage]:
        """
        Obtiene los últimos N mensajes de una sesión.

        Args:
            session_id (str): Identificador de la sesión.
            count (int): Cantidad de mensajes a obtener.

        Returns:
            list[ChatMessage]: Lista de mensajes en orden cronológico.
        """
        messages = (
            self.db.query(ChatMessageModel)
            .filter(ChatMessageModel.session_id == session_id)
            .order_by(ChatMessageModel.timestamp.desc())
            .limit(count)
            .all()
        )

        messages.reverse()
        return [self._model_to_entity(message) for message in messages]

    def _model_to_entity(self, model: ChatMessageModel) -> ChatMessage:
        """
        Convierte un modelo ORM a entidad del dominio.

        Args:
            model (ChatMessageModel): Modelo ORM.

        Returns:
            ChatMessage: Entidad del dominio.
        """
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp,
        )

    def _entity_to_model(self, entity: ChatMessage) -> ChatMessageModel:
        """
        Convierte una entidad del dominio a modelo ORM.

        Args:
            entity (ChatMessage): Entidad del dominio.

        Returns:
            ChatMessageModel: Modelo ORM.
        """
        return ChatMessageModel(
            id=entity.id,
            session_id=entity.session_id,
            role=entity.role,
            message=entity.message,
            timestamp=entity.timestamp,
        )
    