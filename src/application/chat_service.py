"""
Servicio de aplicación para gestionar el chat con IA.

Este módulo contiene la lógica necesaria para procesar mensajes
del usuario, construir contexto conversacional, llamar al servicio
de IA y almacenar el historial del chat.
"""

from datetime import datetime
from typing import List, Optional

from src.application.dtos import (
    ChatHistoryDTO,
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
)
from src.domain.entities import ChatContext, ChatMessage
from src.domain.exceptions import ChatServiceError
from src.domain.repositories import IChatRepository, IProductRepository


class ChatService:
    """
    Servicio de aplicación para gestionar conversaciones con IA.

    Este servicio coordina la recuperación de productos, la memoria
    conversacional y la generación de respuestas del asistente.

    Attributes:
        product_repository (IProductRepository): Repositorio de productos.
        chat_repository (IChatRepository): Repositorio de mensajes del chat.
        ai_service: Servicio externo encargado de generar respuestas.
    """

    def __init__(
        self,
        product_repository: IProductRepository,
        chat_repository: IChatRepository,
        ai_service,
    ) -> None:
        """
        Inicializa el servicio con sus dependencias.

        Args:
            product_repository (IProductRepository): Repositorio de productos.
            chat_repository (IChatRepository): Repositorio del historial de chat.
            ai_service: Servicio de IA que genera respuestas.
        """
        self.product_repository = product_repository
        self.chat_repository = chat_repository
        self.ai_service = ai_service

    async def process_message(
        self,
        request: ChatMessageRequestDTO,
    ) -> ChatMessageResponseDTO:
        """
        Procesa un mensaje del usuario y genera una respuesta del asistente.

        Flujo:
            1. Obtiene productos disponibles.
            2. Obtiene historial reciente de la sesión.
            3. Construye el contexto conversacional.
            4. Solicita una respuesta al servicio de IA.
            5. Guarda mensaje del usuario y respuesta del asistente.
            6. Retorna la respuesta final en formato DTO.

        Args:
            request (ChatMessageRequestDTO): Solicitud con session_id y mensaje.

        Returns:
            ChatMessageResponseDTO: Respuesta generada por el asistente.

        Raises:
            ChatServiceError: Si ocurre un error durante el procesamiento.
        """
        try:
            products = self.product_repository.get_all()
            recent_messages = self.chat_repository.get_recent_messages(
                request.session_id,
                6,
            )
            context = ChatContext(messages=recent_messages)

            assistant_response = await self.ai_service.generate_response(
                user_message=request.message,
                products=products,
                context=context,
            )

            timestamp = datetime.utcnow()

            user_message = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="user",
                message=request.message,
                timestamp=timestamp,
            )

            assistant_message = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="assistant",
                message=assistant_response,
                timestamp=timestamp,
            )

            self.chat_repository.save_message(user_message)
            self.chat_repository.save_message(assistant_message)

            return ChatMessageResponseDTO(
                session_id=request.session_id,
                user_message=request.message,
                assistant_message=assistant_response,
                timestamp=timestamp,
            )
        except Exception as error:
            raise ChatServiceError(
                f"Error al procesar el mensaje del chat: {str(error)}"
            ) from error

    def get_session_history(
        self,
        session_id: str,
        limit: Optional[int] = None,
    ) -> List[ChatHistoryDTO]:
        """
        Obtiene el historial de una sesión de chat.

        Args:
            session_id (str): Identificador de la sesión.
            limit (Optional[int]): Cantidad máxima de mensajes a retornar.

        Returns:
            List[ChatHistoryDTO]: Historial de mensajes en formato DTO.

        Raises:
            ChatServiceError: Si ocurre un error al consultar el historial.
        """
        try:
            messages = self.chat_repository.get_session_history(session_id, limit)
            return [ChatHistoryDTO.model_validate(message) for message in messages]
        except Exception as error:
            raise ChatServiceError(
                f"Error al obtener historial de la sesión: {str(error)}"
            ) from error

    def clear_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión.

        Args:
            session_id (str): Identificador de la sesión.

        Returns:
            int: Cantidad de mensajes eliminados.

        Raises:
            ChatServiceError: Si ocurre un error al eliminar el historial.
        """
        try:
            deleted_count = self.chat_repository.delete_session_history(session_id)
            return deleted_count
        except Exception as error:
            raise ChatServiceError(
                f"Error al eliminar historial de la sesión: {str(error)}"
            ) from error
        