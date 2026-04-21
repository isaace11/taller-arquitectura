"""
DTOs de la capa de aplicación.
Validan y transfieren datos entre la API, servicios y otras capas

"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class ProductDTO(BaseModel):
    """
    DTO para transferir datos de productos.

    Attributes:
        id (Optional[int]): Identificador del producto.
        name (str): Nombre del producto.
        brand (str): Marca del producto.
        category (str): Categoría del producto.
        size (str): Talla del producto.
        color (str): Color del producto.
        price (float): Precio del producto.
        stock (int): Cantidad disponible.
        description (str): Descripción del producto.
    """

    id: Optional[int] = None  
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    @validator("price")
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

    @validator("stock")
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

    class Config:
        """
        Configuración del modelo Pydantic.
        """

        from_attributes = True


class ChatMessageRequestDTO(BaseModel):
    """
    DTO para recibir mensajes del usuario en el chat.

    Attributes:
        session_id (str): Identificador de la sesión.
        message (str): Mensaje enviado por el usuario.
    """

    session_id: str
    message: str

    @validator("message")
    def message_not_empty(cls, value: str) -> str:
        """
        Valida que el mensaje no esté vacío.

        Args:
            value (str): Mensaje a validar.

        Returns:
            str: Mensaje validado.

        Raises:
            ValueError: Si el mensaje está vacío.
        """
        if not value or not value.strip():
            raise ValueError("El mensaje no puede estar vacío")
        return value

    @validator("session_id")
    def session_id_not_empty(cls, value: str) -> str:
        """
        Valida que el identificador de sesión no esté vacío.

        Args:
            value (str): session_id a validar.

        Returns:
            str: session_id validado.

        Raises:
            ValueError: Si el session_id está vacío.
        """
        if not value or not value.strip():
            raise ValueError("El session_id no puede estar vacío")
        return value


class ChatMessageResponseDTO(BaseModel):
    """
    DTO para enviar la respuesta del chat.

    Attributes:
        session_id (str): Identificador de la sesión.
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

    id: int
    role: str
    message: str
    timestamp: datetime

    class Config:
        """
        Configuración del modelo Pydantic.
        """

        from_attributes = True
