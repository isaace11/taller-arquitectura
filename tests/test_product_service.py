import pytest

from src.application.dtos import ProductDTO
from src.application.product_service import ProductService
from src.domain.entities import Product
from src.domain.exceptions import ProductNotFoundError
from src.domain.repositories import IProductRepository


class FakeProductRepository(IProductRepository):
    def __init__(self) -> None:
        self.products = [
            Product(
                id=1,
                name="Nike Air",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=120,
                stock=5,
                description="Zapato para correr",
            ),
            Product(
                id=2,
                name="Puma Classic",
                brand="Puma",
                category="Casual",
                size="40",
                color="Blanco",
                price=80,
                stock=0,
                description="Zapato casual",
            ),
        ]

    def get_all(self):
        return self.products

    def get_by_id(self, product_id):
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def get_by_brand(self, brand):
        return [product for product in self.products if product.brand == brand]

    def get_by_category(self, category):
        return [product for product in self.products if product.category == category]

    def save(self, product):
        if product.id is None:
            product.id = len(self.products) + 1
            self.products.append(product)
        return product

    def delete(self, product_id):
        for index, product in enumerate(self.products):
            if product.id == product_id:
                del self.products[index]
                return True
        return False


@pytest.fixture
def product_service() -> ProductService:
    return ProductService(FakeProductRepository())


def test_get_all_products_returns_dtos(product_service: ProductService) -> None:
    products = product_service.get_all_products()

    assert len(products) == 2
    assert all(isinstance(product, ProductDTO) for product in products)


def test_get_product_by_id_returns_expected_product(product_service: ProductService) -> None:
    product = product_service.get_product_by_id(1)

    assert product.name == "Nike Air"
    assert product.brand == "Nike"


def test_get_product_by_id_raises_when_product_does_not_exist(
    product_service: ProductService,
) -> None:
    with pytest.raises(ProductNotFoundError, match="999"):
        product_service.get_product_by_id(999)


def test_search_products_by_brand_filters_results(product_service: ProductService) -> None:
    products = product_service.search_products(brand="Nike")

    assert len(products) == 1
    assert products[0].brand == "Nike"


def test_get_available_products_returns_only_products_with_stock(
    product_service: ProductService,
) -> None:
    products = product_service.get_available_products()

    assert len(products) == 1
    assert products[0].stock > 0


def test_create_product_persists_valid_product(product_service: ProductService) -> None:
    new_product = ProductDTO(
        name="Adidas Runfalcon",
        brand="Adidas",
        category="Running",
        size="41",
        color="Azul",
        price=99.9,
        stock=4,
        description="Modelo para entrenamiento diario",
    )

    created_product = product_service.create_product(new_product)

    assert created_product.id == 3
    assert created_product.name == "Adidas Runfalcon"


def test_delete_product_removes_existing_product(product_service: ProductService) -> None:
    deleted = product_service.delete_product(1)

    assert deleted is True


def test_delete_product_raises_when_product_does_not_exist(
    product_service: ProductService,
) -> None:
    with pytest.raises(ProductNotFoundError, match="999"):
        product_service.delete_product(999)
