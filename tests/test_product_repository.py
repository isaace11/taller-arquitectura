from src.domain.entities import Product
from src.infrastructure.db.models import ProductModel
from src.infrastructure.repositories.product_repository import SQLProductRepository


def seed_products(db_session) -> None:
    db_session.add_all(
        [
            ProductModel(
                name="Nike Air Zoom",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=120.0,
                stock=5,
                description="Modelo running",
            ),
            ProductModel(
                name="Puma Suede",
                brand="Puma",
                category="Casual",
                size="40",
                color="Blanco",
                price=80.0,
                stock=2,
                description="Modelo casual",
            ),
        ]
    )
    db_session.commit()


def test_get_all_returns_all_products(db_session) -> None:
    seed_products(db_session)
    repository = SQLProductRepository(db_session)

    products = repository.get_all()

    assert len(products) == 2
    assert products[0].name == "Nike Air Zoom"


def test_get_by_id_returns_expected_product(db_session) -> None:
    seed_products(db_session)
    repository = SQLProductRepository(db_session)

    product = repository.get_by_id(1)

    assert product is not None
    assert product.brand == "Nike"


def test_get_by_brand_filters_products(db_session) -> None:
    seed_products(db_session)
    repository = SQLProductRepository(db_session)

    products = repository.get_by_brand("Puma")

    assert len(products) == 1
    assert products[0].name == "Puma Suede"


def test_get_by_category_filters_products(db_session) -> None:
    seed_products(db_session)
    repository = SQLProductRepository(db_session)

    products = repository.get_by_category("Running")

    assert len(products) == 1
    assert products[0].brand == "Nike"


def test_save_creates_new_product_when_id_is_none(db_session) -> None:
    repository = SQLProductRepository(db_session)
    product = Product(
        id=None,
        name="Adidas Duramo",
        brand="Adidas",
        category="Running",
        size="41",
        color="Azul",
        price=95.0,
        stock=4,
        description="Nuevo producto",
    )

    saved_product = repository.save(product)

    assert saved_product.id is not None
    assert saved_product.name == "Adidas Duramo"


def test_save_updates_existing_product(db_session) -> None:
    seed_products(db_session)
    repository = SQLProductRepository(db_session)
    updated = Product(
        id=1,
        name="Nike Air Zoom 2",
        brand="Nike",
        category="Running",
        size="42",
        color="Rojo",
        price=130.0,
        stock=7,
        description="Modelo actualizado",
    )

    saved_product = repository.save(updated)

    assert saved_product.name == "Nike Air Zoom 2"
    assert saved_product.color == "Rojo"
    assert saved_product.stock == 7


def test_delete_removes_existing_product(db_session) -> None:
    seed_products(db_session)
    repository = SQLProductRepository(db_session)

    deleted = repository.delete(1)

    assert deleted is True
    assert repository.get_by_id(1) is None


def test_delete_returns_false_when_product_does_not_exist(db_session) -> None:
    repository = SQLProductRepository(db_session)

    deleted = repository.delete(999)

    assert deleted is False
