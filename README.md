# Image Similarity Search API (Proyecto FastAPI)

## Descripción

Esta es una API REST construida con **FastAPI** que permite a los usuarios subir una imagen y encontrar imágenes visualmente similares dentro de un conjunto de datos predefinido. Utiliza el modelo **CLIP** para generar embeddings (vectores) de las imágenes y **Faiss** para realizar búsquedas eficientes de vecinos más cercanos en el espacio vectorial.

## Características Principales

* **Subida de Imágenes:** Endpoint para subir imágenes vía `multipart/form-data`.
* **Búsqueda de Similitud:** Encuentra las `k` imágenes más similares a la imagen subida.
* **Validación:** Valida el tipo de archivo (MIME type), tamaño máximo y contenido de la imagen subida.
* **Configuración Flexible:** Usa un archivo `.env` y `pydantic-settings` para configurar rutas, modelos, CORS, etc.
* **CORS Habilitado:** Configurable para permitir solicitudes desde frontends en diferentes orígenes.
* **Manejo Centralizado de Errores:** Middleware personalizado para devolver respuestas JSON consistentes en caso de error.
* **Servicio de Imágenes Estáticas:** Sirve los archivos de imagen del dataset para mostrarlos en los resultados.
* **Documentación Automática:** Incluye documentación interactiva de la API vía Swagger UI (`/api/v1/docs`) y ReDoc (`/api/v1/redoc`).

## Tecnología Utilizada

* **Backend:** Python 3.x, FastAPI
* **Servidor ASGI:** Uvicorn
* **Búsqueda Vectorial:** Faiss (CPU o GPU)
* **Embeddings de Imagen:** Modelo CLIP (ej. `ViT-B/32` vía `torch`/`transformers` o similar)
* **Procesamiento de Imagen:** Pillow (PIL)
* **Gestor de Paquetes/Entorno:** uv (de Astral)
* **Configuración:** Pydantic Settings
* **Manejo de Forms:** python-multipart

## Configuración e Instalación

**Prerrequisitos:**

* Python 3.8+
* `uv` instalado (`pip install uv` o sigue instrucciones oficiales de Astral)

**Pasos:**

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/jesujsg/image-similarity-search.git
    cd image-similarity-search
    ```

2.  **Crear Entorno Virtual:**
    ```bash
    uv venv
    ```

3.  **Activar Entorno Virtual:**
    * Linux/macOS: `source .venv/bin/activate`
    * Windows: `.\.venv\Scripts\activate`

4.  **Instalar Dependencias:**
    * Si tienes un archivo `requirements.txt`:
        ```bash
        uv pip install -r requirements.txt
        ```
    * Si no lo tienes, créalo desde el entorno activado después de instalar manualmente las dependencias principales:
        ```bash
        uv add o uv pip install "fastapi[standard]" faiss-cpu pillow torch torchvision torchaudio transformers sentence-transformers pydantic-settings python-multipart
        # Luego genera el archivo:
        uv pip freeze > requirements.txt (No usar en caso de usar solo uv)
        ```

5.  **Variables de Entorno (`.env`):**
    * Crea un archivo llamado `.env` en la raíz del proyecto.

        ```dotenv
        # .env.example - Copia a .env y edita

        # --- Info Proyecto ---
        APP_PROJECT_NAME="Image Similarity Search API"
        APP_PROJECT_VERSION="1.0.0"

        # --- Rutas (¡MUY IMPORTANTE! Usa rutas absolutas o relativas correctas) ---
        APP_INDEX_FAISS_PATH=/ruta/completa/a/data/index/index.faiss
        APP_MAPPING_ROUTES_PATH=/ruta/completa/a/data/index/mapping.json
        APP_STATIC_IMAGE_PATH=/ruta/completa/a/static/images # Directorio que contiene tus imágenes

        # --- Modelo y Dispositivo ---
        APP_CLIP_MODEL_NAME="ViT-B/32" # O el modelo CLIP que uses
        APP_DEVICE="cpu" # o "cuda" si tienes GPU y PyTorch/Faiss con soporte CUDA

        # --- URLs ---
        # URL base para construir las URLs de las imágenes en la respuesta
        # Debe apuntar a donde se sirven los archivos estáticos
        APP_IMAGE_BASE_URL="http://localhost:8000/static" # Ajusta host/puerto/ruta si es necesario

        # --- Límites ---
        APP_MAX_UPLOAD_SIZE=10485760 # 10 MB en bytes

        # --- Configuración CORS ---
        APP_ALLOWED_ORIGINS="http://localhost:3000,[http://127.0.0.1:3000](http://127.0.0.1:3000)"
        APP_ALLOW_CREDENTIALS=True
        APP_ALLOW_METHODS="*"
        APP_ALLOW_HEADERS="*"
        ```