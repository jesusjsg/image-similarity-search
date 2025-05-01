FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \ 
    PIP_NO_CACHE_DIR=0 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app
COPY requirements.txt .
RUN pip install uv && uv pip install --system --no-cache -r requirements.txt
COPY ./app /app/app
EXPOSE 8000
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]