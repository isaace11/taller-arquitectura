import asyncio
from pathlib import Path
from uuid import uuid4

import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.api.main import app
from src.infrastructure.db.database import Base, get_db
from src.infrastructure.db.models import ProductModel
import src.infrastructure.api.main as api_main


class FakeGeminiService:
    async def generate_response(self, user_message: str, products: list, context) -> str:
        return f"Respuesta simulada para: {user_message}"


def configure_test_app(monkeypatch) -> None:
    temp_dir = Path("tests/.tmp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    db_path = temp_dir / f"test_api_{uuid4().hex}.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    session = testing_session_local()
    session.add_all(
        [
            ProductModel(
                name="Nike Air Zoom Pegasus",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=120.0,
                stock=5,
                description="Zapato de running con excelente amortiguacion.",
            ),
            ProductModel(
                name="Puma Suede Classic",
                brand="Puma",
                category="Casual",
                size="40",
                color="Blanco",
                price=80.0,
                stock=0,
                description="Zapato casual clasico para uso diario.",
            ),
        ]
    )
    session.commit()
    session.close()

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    monkeypatch.setattr(api_main, "GeminiService", FakeGeminiService)
    monkeypatch.setattr(api_main, "init_db", lambda: None)
    app.dependency_overrides[get_db] = override_get_db


async def get_async_client() -> httpx.AsyncClient:
    transport = httpx.ASGITransport(app=app)
    return httpx.AsyncClient(transport=transport, base_url="http://testserver")


def test_read_root_returns_available_endpoints(monkeypatch) -> None:
    configure_test_app(monkeypatch)

    async def run_test():
        async with await get_async_client() as client:
            response = await client.get("/")
            assert response.status_code == 200
            data = response.json()
            assert data["version"] == "1.0.0"
            assert "/products" in data["endpoints"]

    asyncio.run(run_test())


def test_health_check_returns_ok_status(monkeypatch) -> None:
    configure_test_app(monkeypatch)

    async def run_test():
        async with await get_async_client() as client:
            response = await client.get("/health")
            assert response.status_code == 200
            assert response.json()["status"] == "ok"

    asyncio.run(run_test())


def test_get_products_returns_seeded_products(monkeypatch) -> None:
    configure_test_app(monkeypatch)

    async def run_test():
        async with await get_async_client() as client:
            response = await client.get("/products")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["name"] == "Nike Air Zoom Pegasus"

    asyncio.run(run_test())


def test_get_product_by_id_returns_404_when_product_does_not_exist(monkeypatch) -> None:
    configure_test_app(monkeypatch)

    async def run_test():
        async with await get_async_client() as client:
            response = await client.get("/products/999")
            assert response.status_code == 404
            assert "no encontrado" in response.json()["detail"].lower()

    asyncio.run(run_test())


def test_chat_endpoint_generates_and_persists_response(monkeypatch) -> None:
    configure_test_app(monkeypatch)

    async def run_test():
        async with await get_async_client() as client:
            response = await client.post(
                "/chat",
                json={
                    "session_id": "cliente-001",
                    "message": "Busco zapatos para correr",
                },
            )
            assert response.status_code == 200
            data = response.json()
            assert data["session_id"] == "cliente-001"
            assert "Respuesta simulada" in data["assistant_message"]

    asyncio.run(run_test())


def test_chat_history_endpoint_returns_saved_messages(monkeypatch) -> None:
    configure_test_app(monkeypatch)

    async def run_test():
        async with await get_async_client() as client:
            await client.post(
                "/chat",
                json={
                    "session_id": "cliente-001",
                    "message": "Busco zapatos para correr",
                },
            )
            response = await client.get("/chat/history/cliente-001")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["role"] == "user"
            assert data[1]["role"] == "assistant"

    asyncio.run(run_test())


def test_delete_chat_history_removes_saved_messages(monkeypatch) -> None:
    configure_test_app(monkeypatch)

    async def run_test():
        async with await get_async_client() as client:
            await client.post(
                "/chat",
                json={
                    "session_id": "cliente-001",
                    "message": "Busco zapatos para correr",
                },
            )
            delete_response = await client.delete("/chat/history/cliente-001")
            history_response = await client.get("/chat/history/cliente-001")
            assert delete_response.status_code == 200
            assert delete_response.json()["deleted_messages"] == 2
            assert history_response.status_code == 200
            assert history_response.json() == []

    asyncio.run(run_test())
