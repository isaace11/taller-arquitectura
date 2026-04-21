"""
Configuración global de la aplicación.

"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Clase que encapsula la configuración global de la aplicación.

    
    """

    def __init__(self) -> None:
        """
        Inicializa la configuración cargando variables de entorno.
        """
        self.gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
        self.database_url: str = os.getenv(
            "DATABASE_URL",
            "sqlite:///./data/ecommerce_chat.db",
        )
        self.environment: str = os.getenv("ENVIRONMENT", "development")


settings = Settings()