"""
DTOs de la capa de aplicacion.
Validan y transfieren datos entre la API, servicios y otras capas.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class ProductDTO(BaseModel):
    """
    DTO para transferir datos de productos.

    Attributes:
        id (Optional[int]): Identificador del producto.
        name (str): Nombre del producto.
        brand (str): Marca del producto.
        category (str): Categoria del producto.
        size (str): Talla del producto.
        color (str): Color del producto.
        price (float): Precio del producto.
        stock (int): Cantidad disponible.
        description (str): Descripcion del producto.
    """

    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, value: float) -> float:
        """
        Valida que el precio sea mayor a cero.

        Args:
            value (float): Precio a validar.

        Returns:
            float: Precio validado.

        Raises:
            ValueError: Si el precio es menor o igual a cero.
        """
        if value <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return value

    @field_validator("stock")
    @classmethod
    def stock_must_be_non_negative(cls, value: int) -> int:
        """
        Valida que el stock no sea negativo.

        Args:
            value (int): Stock a validar.

        Returns:
            int: Stock validado.

        Raises:
            ValueError: Si el stock es negativo.
        """
        if value < 0:
            raise ValueError("El stock no puede ser negativo")
        return value


class ChatMessageRequestDTO(BaseModel):
    """
    DTO para recibir mensajes del usuario en el chat.

    Attributes:
        session_id (str): Identificador de la sesion.
        message (str): Mensaje enviado por el usuario.
    """

    session_id: str
    message: str

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, value: str) -> str:
        """
        Valida que el mensaje no este vacio.

        Args:
            value (str): Mensaje a validar.

        Returns:
            str: Mensaje validado.

        Raises:
            ValueError: Si el mensaje esta vacio.
        """
        if not value or not value.strip():
            raise ValueError("El mensaje no puede estar vacio")
        return value

    @field_validator("session_id")
    @classmethod
    def session_id_not_empty(cls, value: str) -> str:
        """
        Valida que el identificador de sesion no este vacio.

        Args:
            value (str): session_id a validar.

        Returns:
            str: session_id validado.

        Raises:
            ValueError: Si el session_id esta vacio.
        """
        if not value or not value.strip():
            raise ValueError("El session_id no puede estar vacio")
        return value


class ChatMessageResponseDTO(BaseModel):
    """
    DTO para enviar la respuesta del chat.

    Attributes:
        session_id (str): Identificador de la sesion.
        user_message (str): Mensaje enviado por el usuario.
        assistant_message (str): Respuesta generada por el asistente.
        timestamp (datetime): Fecha y hora de la respuesta.
    """

    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime


class ChatHistoryDTO(BaseModel):
    """
    DTO para representar un mensaje del historial de chat.

    Attributes:
        id (int): Identificador del mensaje.
        role (str): Rol del mensaje, user o assistant.
        message (str): Contenido del mensaje.
        timestamp (datetime): Fecha y hora del mensaje.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    message: str
    timestamp: datetime
