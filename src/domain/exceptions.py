"""
excepciones específicas del dominio 
tienes los errores de negocio y permiten comunicar
situaciones inválidas de forma clara
"""
class ProductNotFoundError(Exception):
    """
    Excepción lanzada cuando no se encuentra un producto.
    """

    def __init__(self, product_id: int = None):
        """
        Inicializa la excepción con un mensaje descriptivo.

        Args:
            product_id (int, optional): Identificador del producto no encontrado.
        """
        if product_id is not None:
            message = f"Producto con ID {product_id} no encontrado"
        else:
            message = "Producto no encontrado"

        super().__init__(message)


class InvalidProductDataError(Exception):
    """
    Excepción lanzada cuando los datos de un producto son inválidos.
    """

    def __init__(self, message: str = "Datos de producto inválidos"):
        """
        Inicializa la excepción con un mensaje personalizado.

        Args:
            message (str): Mensaje descriptivo del error.
        """
        super().__init__(message)


class ChatServiceError(Exception):
    """
    Excepción lanzada cuando ocurre un error en el servicio de chat.
    """

    def __init__(self, message: str = "Error en el servicio de chat"):
        """
        Inicializa la excepción con un mensaje personalizado.

        Args:
            message (str): Mensaje descriptivo del error.
        """
        super().__init__(message)
        