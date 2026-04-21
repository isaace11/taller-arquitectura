"""
Repositorio de productos usando SQLAlchemy.

Implementa el contrato definido en la capa de dominio
para gestionar productos en la base de datos.
"""

from sqlalchemy.orm import Session

from src.domain.entities import Product
from src.domain.repositories import IProductRepository
from src.infrastructure.db.models import ProductModel


class SQLProductRepository(IProductRepository):
    """
    Implementación concreta del repositorio de productos.

    Attributes:
        db (Session): Sesión activa de base de datos.
    """

    def __init__(self, db: Session) -> None:
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db (Session): Sesión SQLAlchemy.
        """
        self.db = db

    def get_all(self) -> list[Product]:
        """
        Obtiene todos los productos.

        Returns:
            list[Product]: Lista de entidades Product.
        """
        products = self.db.query(ProductModel).all()
        return [self._model_to_entity(product) for product in products]

    def get_by_id(self, product_id: int) -> Product | None:
        """
        Obtiene un producto por ID.

        Args:
            product_id (int): Identificador del producto.

        Returns:
            Product | None: Producto encontrado o None.
        """
        product = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if product is None:
            return None
        return self._model_to_entity(product)

    def get_by_brand(self, brand: str) -> list[Product]:
        """
        Obtiene productos por marca.

        Args:
            brand (str): Marca a consultar.

        Returns:
            list[Product]: Lista de productos de esa marca.
        """
        products = self.db.query(ProductModel).filter(ProductModel.brand == brand).all()
        return [self._model_to_entity(product) for product in products]

    def get_by_category(self, category: str) -> list[Product]:
        """
        Obtiene productos por categoría.

        Args:
            category (str): Categoría a consultar.

        Returns:
            list[Product]: Lista de productos de esa categoría.
        """
        products = self.db.query(ProductModel).filter(ProductModel.category == category).all()
        return [self._model_to_entity(product) for product in products]

    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto.

        Args:
            product (Product): Producto a persistir.

        Returns:
            Product: Producto guardado con su ID.
        """
        if product.id is None:
            product_model = self._entity_to_model(product)
            self.db.add(product_model)
            self.db.commit()
            self.db.refresh(product_model)
            return self._model_to_entity(product_model)

        existing_model = self.db.query(ProductModel).filter(ProductModel.id == product.id).first()

        if existing_model is None:
            product_model = self._entity_to_model(product)
            self.db.add(product_model)
            self.db.commit()
            self.db.refresh(product_model)
            return self._model_to_entity(product_model)

        existing_model.name = product.name
        existing_model.brand = product.brand
        existing_model.category = product.category
        existing_model.size = product.size
        existing_model.color = product.color
        existing_model.price = product.price
        existing_model.stock = product.stock
        existing_model.description = product.description

        self.db.commit()
        self.db.refresh(existing_model)

        return self._model_to_entity(existing_model)

    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto por ID.

        Args:
            product_id (int): Identificador del producto.

        Returns:
            bool: True si se eliminó, False si no existía.
        """
        product = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()

        if product is None:
            return False

        self.db.delete(product)
        self.db.commit()
        return True

    def _model_to_entity(self, model: ProductModel) -> Product:
        """
        Convierte un modelo ORM a una entidad del dominio.

        Args:
            model (ProductModel): Modelo ORM.

        Returns:
            Product: Entidad de dominio.
        """
        return Product(
            id=model.id,
            name=model.name,
            brand=model.brand,
            category=model.category,
            size=model.size,
            color=model.color,
            price=model.price,
            stock=model.stock,
            description=model.description,
        )

    def _entity_to_model(self, entity: Product) -> ProductModel:
        """
        Convierte una entidad del dominio a modelo ORM.

        Args:
            entity (Product): Entidad del dominio.

        Returns:
            ProductModel: Modelo ORM.
        """
        return ProductModel(
            id=entity.id,
            name=entity.name,
            brand=entity.brand,
            category=entity.category,
            size=entity.size,
            color=entity.color,
            price=entity.price,
            stock=entity.stock,
            description=entity.description,
        )
    