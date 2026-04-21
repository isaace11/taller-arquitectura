from src.application.product_service import ProductService
from src.domain.entities import Product
from src.domain.repositories import IProductRepository


class FakeProductRepository(IProductRepository):
    def __init__(self):
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
        return product

    def delete(self, product_id):
        return any(product.id == product_id for product in self.products)


repo = FakeProductRepository()
service = ProductService(repo)

print("TODOS:")
print(service.get_all_products())

print("\nPRODUCTO ID 1:")
print(service.get_product_by_id(1))

print("\nDISPONIBLES:")
print(service.get_available_products())
