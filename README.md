# E-commerce con Chat IA

API REST de e-commerce de zapatos con chat inteligente construida con Clean Architecture, FastAPI, SQLAlchemy, SQLite y Google Gemini.

## Características
- API REST para gestión de productos
- Chatbot con Google Gemini
- Historial conversacional persistente con SQLite
- Arquitectura limpia (Domain, Application, Infrastructure)
- Contenerización con Docker
- Documentación asertiva con Swagger

## Descripcion

Este proyecto implementa una tienda de zapatos con dos funcionalidades principales:

- Consulta de productos mediante endpoints REST.
- Asistente conversacional con IA que recomienda productos usando el inventario disponible y el historial reciente del chat.

La aplicacion esta organizada en capas para separar dominio, aplicacion e infraestructura.

## Arquitectura

El proyecto sigue una estructura basada en Clean Architecture:

- `src/domain`: entidades, excepciones e interfaces de repositorios.
- `src/application`: DTOs y servicios de aplicacion.
- `src/infrastructure`: API FastAPI, repositorios SQLAlchemy, base de datos y proveedor Gemini.
- `tests`: pruebas unitarias y de integracion.

## Tecnologias

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Google Gemini
- Docker
- Pytest
- Pytest Cov

## Requisitos previos

- Python 3.12 o superior
- Docker Desktop
- API Key de Google Gemini

## Variables de entorno

Crea un archivo `.env` a partir de `.env.example`:

```env
GEMINI_API_KEY=tu_api_key_aqui
DATABASE_URL=sqlite:///./data/ecommerce_chat.db
ENVIRONMENT=development
```

## Instalacion local

1. Clonar el repositorio

```powershell
git clone https://github.com/isaace11/taller-arquitectura.git
cd taller-arquitectura
```

2. Crear entorno virtual

```powershell
python -m venv venv
```

3. Activar entorno virtual

```powershell
.\venv\Scripts\Activate.ps1
```

4. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

5. Configurar variables de entorno

```powershell
Copy-Item .env.example .env
```

Despues edita `.env` y agrega tu `GEMINI_API_KEY`.

## Ejecucion local

Para ejecutar la API sin Docker:

```powershell
.\venv\Scripts\python.exe -m uvicorn src.infrastructure.api.main:app --reload
```

La aplicacion quedara disponible en:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Ejecucion con Docker

Construir y levantar el contenedor:

```powershell
docker compose up --build -d
```

Ver estado del contenedor:

```powershell
docker compose ps
```

Ver logs:

```powershell
docker compose logs -f
```

Detener el entorno:

```powershell
docker compose down
```

## Endpoints principales

- `GET /`
- `GET /products`
- `GET /products/{product_id}`
- `POST /chat`
- `GET /chat/history/{session_id}`
- `DELETE /chat/history/{session_id}`
- `GET /health`


# Flujo de la app:
Cliente -> FastAPI -> Servicios de Aplicación (Gemini) -> Repositorios -> SQLite

## Ejemplos de uso

### Obtener productos

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/products | Select-Object -ExpandProperty Content
```

### Enviar mensaje al chat

```powershell
Invoke-WebRequest `
  -UseBasicParsing `
  -Uri http://127.0.0.1:8000/chat `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"session_id":"cliente-001","message":"Busco zapatos Nike para correr talla 42"}' |
  Select-Object -ExpandProperty Content
```

### Consultar historial

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/chat/history/cliente-001 | Select-Object -ExpandProperty Content
```

## Pruebas

Ejecutar pruebas:

```powershell
.\venv\Scripts\python.exe -m pytest
```

Ejecutar pruebas con coverage:

```powershell
.\venv\Scripts\python.exe -m pytest --cov=src --cov-report=term-missing
```

Estado actual de pruebas:

- `38 passed`
- `83%` de coverage total

## Estructura del proyecto

```text
taller-arquitectura/
+-- data/
+-- src/
|   +-- application/
|   +-- domain/
|   +-- infrastructure/
+-- tests/
+-- .env.example
+-- Dockerfile
+-- docker-compose.yml
+-- requirements.txt
+-- evidencias/
+-- README.md
```

## Evidencias

Las capturas del taller deben guardarse en la carpeta `evidencias/` con estos nombres:

- `evidencias/01-swagger-ui-1.png`
- `evidencias/01-swagger-ui-2.png`
- `evidencias/02-docker-logs.png`
- `evidencias/03-docker-running.png`
- `evidencias/04-api-call-products-1.png`
- `evidencias/04-api-call-products-2.png`
- `evidencias/05-api-call-chat-1.png`
- `evidencias/05-api-call-chat-2.png`
- `evidencias/06-database-1.png`
- `evidencias/06-database-2.png`

### Checklist de evidencias


## Comandos usados para ver evidencias:

### Ver logs de Docker

```powershell
docker compose logs
```

### Ver contenedor corriendo

```powershell
docker compose ps
```

### Consumir `/products`

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/products | Select-Object -ExpandProperty Content
```

### Consumir `/chat`

```powershell
Invoke-WebRequest `
  -UseBasicParsing `
  -Uri http://127.0.0.1:8000/chat `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"session_id":"cliente1","message":"Hola, busco zapatos para una salida casual"}' |
  Select-Object -ExpandProperty Content
```

## Hecho por:

Isabel Acevedo Acosta. 24/04/26


