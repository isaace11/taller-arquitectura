"""
Servicio de integración con Google Gemini.

Este módulo genera respuestas del asistente usando Gemini
a partir del mensaje del usuario, los productos disponibles
y el contexto conversacional.
"""

from google import genai

from src.config import settings
from src.domain.entities import ChatContext


class GeminiService:
    """
    Servicio encargado de generar respuestas usando Google Gemini.
    """

    def __init__(self) -> None:
        """
        Inicializa el cliente de Gemini con la API key configurada.

        Raises:
            ValueError: Si no se encuentra configurada la API key.
        """
        if not settings.gemini_api_key:
            raise ValueError("No se encontró GEMINI_API_KEY en las variables de entorno")

        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_name = "gemini-2.5-flash"

    async def generate_response(
        self,
        user_message: str,
        products: list,
        context: ChatContext,
    ) -> str:
        """
        Genera una respuesta usando Gemini.

        Args:
            user_message (str): Mensaje enviado por el usuario.
            products (list): Lista de productos disponibles.
            context (ChatContext): Contexto conversacional reciente.

        Returns:
            str: Respuesta generada por Gemini.
        """
        products_text = self._format_products(products)
        context_text = context.format_for_prompt()

        prompt = f"""
Eres un asistente virtual experto en ventas de zapatos para un e-commerce.
Tu objetivo es ayudar al cliente a encontrar productos adecuados según sus necesidades.

PRODUCTOS DISPONIBLES:
{products_text}

CONTEXTO DE LA CONVERSACIÓN:
{context_text if context_text else "No hay mensajes previos."}

MENSAJE ACTUAL DEL USUARIO:
{user_message}

INSTRUCCIONES:
- Responde en español.
- Sé amable, claro y útil.
- Recomienda productos solo de la lista disponible.
- Menciona precio, talla, color y stock si es relevante.
- Si el usuario pregunta algo fuera del catálogo, responde honestamente.
- No inventes productos que no estén en la lista.

RESPUESTA:
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )

        return response.text.strip() if response.text else "No pude generar una respuesta en este momento."

    def _format_products(self, products: list) -> str:
        """
        Convierte la lista de productos a texto para incluirla en el prompt.

        Args:
            products (list): Lista de productos del dominio.

        Returns:
            str: Texto formateado con los productos.
        """
        if not products:
            return "No hay productos disponibles."

        lines = []
        for product in products:
            lines.append(
                f"- {product.name} | Marca: {product.brand} | "
                f"Categoría: {product.category} | Talla: {product.size} | "
                f"Color: {product.color} | Precio: ${product.price} | "
                f"Stock: {product.stock} | Descripción: {product.description}"
            )

        return "\n".join(lines)