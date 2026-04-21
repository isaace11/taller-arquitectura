"""
Entidades del dominio (logica y conceptos principales del negocio).

"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Product:
    """
    Entidad que representa un producto en el e-commerce.
    """
    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    def __post_init__(self):
        """
        Validaciones de negocio al crear el producto.
        """
        if not self.name:
            raise ValueError("El nombre del producto no puede estar vacío")

        if self.price <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")

    def is_available(self) -> bool:
        """
        Retorna True si el producto tiene stock disponible.
        """
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce el stock del producto.
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")

        if quantity > self.stock:
            raise ValueError("No hay suficiente stock disponible")

        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """
        Aumenta el stock del producto.
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")

        self.stock += quantity


@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje en el chat.
    """
    id: Optional[int]
    session_id: str
    role: str  # 'user' o 'assistant'
    message: str
    timestamp: datetime

    def __post_init__(self):
        if self.role not in ["user", "assistant"]:
            raise ValueError("El rol debe ser 'user' o 'assistant'")

        if not self.message:
            raise ValueError("El mensaje no puede estar vacío")

        if not self.session_id:
            raise ValueError("El session_id no puede estar vacío")

    def is_from_user(self) -> bool:
        return self.role == "user"

    def is_from_assistant(self) -> bool:
        return self.role == "assistant"


@dataclass
class ChatContext:
    """
    Representa el contexto conversacional (memoria del chat).
    """
    messages: List[ChatMessage]
    max_messages: int = 6

    def get_recent_messages(self) -> List[ChatMessage]:
        """
        Retorna los últimos N mensajes.
        """
        return self.messages[-self.max_messages:]

    def format_for_prompt(self) -> str:
        """
        Convierte el historial a texto para la IA.
        """
        history = []

        for msg in self.get_recent_messages():
            role = "Usuario" if msg.role == "user" else "Asistente"
            history.append(f"{role}: {msg.message}")

        return "\n".join(history)
    