"""
Servicio de aplicación para la gestión de productos.

Este módulo contiene la lógica de aplicación relacionada con
la consulta, creación, actualización y eliminación de productos.
"""

from typing import List, Optional

from src.application.dtos import ProductDTO
from src.domain.entities import Product
from src.domain.exceptions import InvalidProductDataError, ProductNotFoundError
from src.domain.repositories import IProductRepository


class ProductService:
    """
    Servicio de aplicación para gestionar productos.

    Este servicio coordina la interacción entre los DTOs y el
    repositorio de productos, aplicando reglas de negocio de alto nivel.

    Attributes:
        product_repository (IProductRepository): Repositorio de productos.
    """

    def __init__(self, product_repository: IProductRepository) -> None:
        """
        Inicializa el servicio con un repositorio de productos.

        Args:
            product_repository (IProductRepository): Implementación concreta
                del repositorio de productos.
        """
        self.product_repository = product_repository

    def get_all_products(self) -> List[ProductDTO]:
        """
        Obtiene todos los productos del sistema.

        Returns:
            List[ProductDTO]: Lista de productos convertidos a DTO.
        """
        products = self.product_repository.get_all()
        return [ProductDTO.model_validate(product) for product in products]

    def get_product_by_id(self, product_id: int) -> ProductDTO:
        """
        Obtiene un producto por su identificador.

        Args:
            product_id (int): Identificador del producto.

        Returns:
            ProductDTO: Producto encontrado.

        Raises:
            ProductNotFoundError: Si el producto no existe.
        """
        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise ProductNotFoundError(product_id)

        return ProductDTO.model_validate(product)

    def search_products(
        self,
        brand: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[ProductDTO]:
        """
        Busca productos por marca o categoría.

        Si se proporciona marca, filtra por marca.
        Si se proporciona categoría, filtra por categoría.
        Si no se proporciona ningún filtro, retorna todos los productos.

        Args:
            brand (Optional[str]): Marca a buscar.
            category (Optional[str]): Categoría a buscar.

        Returns:
            List[ProductDTO]: Lista de productos encontrados.
        """
        if brand:
            products = self.product_repository.get_by_brand(brand)
        elif category:
            products = self.product_repository.get_by_category(category)
        else:
            products = self.product_repository.get_all()

        return [ProductDTO.model_validate(product) for product in products]

    def create_product(self, product_dto: ProductDTO) -> ProductDTO:
        """
        Crea un nuevo producto.

        Args:
            product_dto (ProductDTO): Datos del producto a crear.

        Returns:
            ProductDTO: Producto creado y guardado.

        Raises:
            InvalidProductDataError: Si ocurre un error al construir la entidad.
        """
        try:
            product = Product(
                id=None,
                name=product_dto.name,
                brand=product_dto.brand,
                category=product_dto.category,
                size=product_dto.size,
                color=product_dto.color,
                price=product_dto.price,
                stock=product_dto.stock,
                description=product_dto.description,
            )
        except ValueError as error:
            raise InvalidProductDataError(str(error)) from error

        saved_product = self.product_repository.save(product)
        return ProductDTO.model_validate(saved_product)

    def update_product(self, product_id: int, product_dto: ProductDTO) -> ProductDTO:
        """
        Actualiza un producto existente.

        Args:
            product_id (int): Identificador del producto a actualizar.
            product_dto (ProductDTO): Nuevos datos del producto.

        Returns:
            ProductDTO: Producto actualizado.

        Raises:
            ProductNotFoundError: Si el producto no existe.
            InvalidProductDataError: Si los datos del producto son inválidos.
        """
        existing_product = self.product_repository.get_by_id(product_id)

        if existing_product is None:
            raise ProductNotFoundError(product_id)

        try:
            updated_product = Product(
                id=product_id,
                name=product_dto.name,
                brand=product_dto.brand,
                category=product_dto.category,
                size=product_dto.size,
                color=product_dto.color,
                price=product_dto.price,
                stock=product_dto.stock,
                description=product_dto.description,
            )
        except ValueError as error:
            raise InvalidProductDataError(str(error)) from error

        saved_product = self.product_repository.save(updated_product)
        return ProductDTO.model_validate(saved_product)

    def delete_product(self, product_id: int) -> bool:
        """
        Elimina un producto por su identificador.

        Args:
            product_id (int): Identificador del producto.

        Returns:
            bool: True si el producto fue eliminado.

        Raises:
            ProductNotFoundError: Si el producto no existe.
        """
        deleted = self.product_repository.delete(product_id)

        if not deleted:
            raise ProductNotFoundError(product_id)

        return True

    def get_available_products(self) -> List[ProductDTO]:
        """
        Obtiene únicamente los productos con stock disponible.

        Returns:
            List[ProductDTO]: Lista de productos disponibles.
        """
        products = self.product_repository.get_all()
        available_products = [product for product in products if product.is_available()]
        return [ProductDTO.model_validate(product) for product in available_products]
    