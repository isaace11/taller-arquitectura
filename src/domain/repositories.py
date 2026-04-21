"""
repositorios del dominio
para definir contraros que deben implementar las clases
de infraestructura con el fin de acceder a los datos.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from .entities import Product, ChatMessage


class IProductRepository(ABC):
    """
    Interface que define el contrato para acceder a productos.
    """

    @abstractmethod
    def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos disponibles en el sistema.

        Returns:
            List[Product]: Lista de productos.
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por su identificador.

        Args:
            product_id (int): Identificador del producto.

        Returns:
            Optional[Product]: Producto encontrado o None si no existe.
        """
        pass

    @abstractmethod
    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene productos filtrados por marca.

        Args:
            brand (str): Marca a consultar.

        Returns:
            List[Product]: Lista de productos de la marca indicada.
        """
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        """
        Obtiene productos filtrados por categoría.

        Args:
            category (str): Categoría a consultar.

        Returns:
            List[Product]: Lista de productos de la categoría indicada.
        """
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto.

        Args:
            product (Product): Producto a guardar.

        Returns:
            Product: Producto guardado o actualizado.
        """
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto por su identificador.

        Args:
            product_id (int): Identificador del producto.

        Returns:
            bool: True si se eliminó, False si no existía.
        """
        pass


class IChatRepository(ABC):
    """
    Interface que define el contrato para gestionar
    el historial de conversaciones.
    """

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje del chat.

        Args:
            message (ChatMessage): Mensaje a guardar.

        Returns:
            ChatMessage: Mensaje guardado con su identificador.
        """
        pass

    @abstractmethod
    def get_session_history(
        self,
        session_id: str,
        limit: Optional[int] = None,
    ) -> List[ChatMessage]:
        """
        Obtiene el historial completo de una sesión.

        Args:
            session_id (str): Identificador de la sesión.
            limit (Optional[int]): Número máximo de mensajes a retornar.

        Returns:
            List[ChatMessage]: Historial de mensajes en orden cronológico.
        """
        pass

    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión.

        Args:
            session_id (str): Identificador de la sesión.

        Returns:
            int: Cantidad de mensajes eliminados.
        """
        pass

    @abstractmethod
    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Obtiene los últimos mensajes de una sesión.

        Args:
            session_id (str): Identificador de la sesión.
            count (int): Cantidad de mensajes a recuperar.

        Returns:
            List[ChatMessage]: Lista de mensajes recientes en orden cronológico.
        """
        pass
    