# ---------- STAGE 1: builder (compila dependencias que requieren Rust/C/C++) ----------
FROM python:3.11-slim AS builder

# Evitar prompts
ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

# instalar dependencias del sistema necesarias para construir paquetes y PostgreSQL client libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    curl \
    ca-certificates \
    git \
    pkg-config \
    libssl-dev \
  && rm -rf /var/lib/apt/lists/*

# Instalar rustup + toolchain (no interactivo)
# el instalador de rustup puede modificar el PATH; añadimos los binarios al PATH
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
# asegurar que rust esté disponible
RUN rustup default stable

# directorio de la app
WORKDIR /app

# copiar archivos necesarios para construir dependencias
COPY requirements.txt /app/

# crear wheelhouse: compilar todas las dependencias en ruedas
# si usas requirements.txt:
RUN if [ -f requirements.txt ]; then \
      python -m pip install --upgrade pip wheel setuptools; \
      python -m pip wheel -r requirements.txt -w /wheels; \
    fi

# si usas Poetry o pyproject.toml, podrías compilar de forma equivalente
# copiar el resto del código (después de compilar ruedas para aprovechar cache)
COPY . /app

# ---------- STAGE 2: final (runtime) ----------
FROM python:3.11-slim

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1

# instalar dependencias mínimas en runtime (libpq)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copiar las ruedas ya construidas desde builder (si existen)
COPY --from=builder /wheels /wheels

# copiar código de la app
COPY --from=builder /app /app

# instalar pip y las ruedas (si /wheels contiene cosas, se instalan desde ahí)
RUN python -m pip install --upgrade pip \
  && if [ -d /wheels ] && [ "$(ls -A /wheels)" ]; then \
       python -m pip install /wheels/*; \
     elif [ -f requirements.txt ]; then \
       python -m pip install -r requirements.txt; \
     fi

# copiar ejemplo de env (opcional) - normalmente NO metas .env en la imagen final.
# Si quieres que la imagen tenga un .env por defecto, descomenta:
# COPY .env.example .env

# Exponer puerto (UVICORN usa por defecto 8000)
EXPOSE 8000

# Comando por defecto (modo desarrollo: recarga automática)
# Si vas a producción, reemplaza --reload por gunicorn/uvicorn sin --reload.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
