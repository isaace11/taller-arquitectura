"""
Aplicación principal FastAPI del proyecto.

Expone los endpoints de productos, chat e información básica
del sistema.
"""

from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.application.chat_service import ChatService
from src.application.dtos import (
    ChatHistoryDTO,
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
    ProductDTO,
)
from src.application.product_service import ProductService
from src.domain.exceptions import ChatServiceError, ProductNotFoundError
from src.infrastructure.db.database import get_db
from src.infrastructure.db.init_db import init_db
from src.infrastructure.llm_providers.gemini_service import GeminiService
from src.infrastructure.repositories.chat_repository import SQLChatRepository
from src.infrastructure.repositories.product_repository import SQLProductRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Inicializa recursos al arrancar la aplicación.

    Args:
        app (FastAPI): Instancia de la aplicación.

    Yields:
        None
    """
    init_db()
    yield


app = FastAPI(
    title="E-commerce Chat IA",
    description="API REST de e-commerce de zapatos con chat inteligente.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def read_root() -> dict:
    """
    Retorna información básica de la API.

    Returns:
        dict: Información general y endpoints disponibles.
    """
    return {
        "message": "Bienvenido a la API de E-commerce con Chat IA",
        "version": "1.0.0",
        "endpoints": [
            "/products",
            "/products/{product_id}",
            "/chat",
            "/chat/history/{session_id}",
            "/health",
        ],
    }


@app.get("/products", response_model=List[ProductDTO])
def get_products(db: Session = Depends(get_db)) -> List[ProductDTO]:
    """
    Obtiene la lista completa de productos.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        List[ProductDTO]: Lista de productos.
    """
    repository = SQLProductRepository(db)
    service = ProductService(repository)
    return service.get_all_products()


@app.get("/products/{product_id}", response_model=ProductDTO)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)) -> ProductDTO:
    """
    Obtiene un producto por su identificador.

    Args:
        product_id (int): Identificador del producto.
        db (Session): Sesión de base de datos.

    Returns:
        ProductDTO: Producto encontrado.

    Raises:
        HTTPException: Si el producto no existe.
    """
    repository = SQLProductRepository(db)
    service = ProductService(repository)

    try:
        return service.get_product_by_id(product_id)
    except ProductNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@app.post("/chat", response_model=ChatMessageResponseDTO)
async def process_chat_message(
    request: ChatMessageRequestDTO,
    db: Session = Depends(get_db),
) -> ChatMessageResponseDTO:
    """
    Procesa un mensaje del usuario y retorna una respuesta del asistente.

    Args:
        request (ChatMessageRequestDTO): Mensaje del usuario.
        db (Session): Sesión de base de datos.

    Returns:
        ChatMessageResponseDTO: Respuesta del asistente.

    Raises:
        HTTPException: Si ocurre un error procesando el chat.
    """
    product_repository = SQLProductRepository(db)
    chat_repository = SQLChatRepository(db)
    ai_service = GeminiService()

    service = ChatService(
        product_repository=product_repository,
        chat_repository=chat_repository,
        ai_service=ai_service,
    )

    try:
        return await service.process_message(request)
    except ChatServiceError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.get("/chat/history/{session_id}", response_model=List[ChatHistoryDTO])
def get_chat_history(
    session_id: str,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> List[ChatHistoryDTO]:
    """
    Obtiene el historial de una sesión de chat.

    Args:
        session_id (str): Identificador de la sesión.
        limit (int): Cantidad máxima de mensajes.
        db (Session): Sesión de base de datos.

    Returns:
        List[ChatHistoryDTO]: Historial de mensajes.
    """
    product_repository = SQLProductRepository(db)
    chat_repository = SQLChatRepository(db)
    ai_service = GeminiService()

    service = ChatService(
        product_repository=product_repository,
        chat_repository=chat_repository,
        ai_service=ai_service,
    )

    return service.get_session_history(session_id, limit)


@app.delete("/chat/history/{session_id}")
def delete_chat_history(session_id: str, db: Session = Depends(get_db)) -> dict:
    """
    Elimina el historial completo de una sesión.

    Args:
        session_id (str): Identificador de la sesión.
        db (Session): Sesión de base de datos.

    Returns:
        dict: Cantidad de mensajes eliminados.
    """
    product_repository = SQLProductRepository(db)
    chat_repository = SQLChatRepository(db)
    ai_service = GeminiService()

    service = ChatService(
        product_repository=product_repository,
        chat_repository=chat_repository,
        ai_service=ai_service,
    )

    deleted_count = service.clear_session_history(session_id)
    return {"deleted_messages": deleted_count}


@app.get("/health")
def health_check() -> dict:
    """
    Endpoint de verificación de salud de la API.

    Returns:
        dict: Estado actual del servicio.
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
    }
