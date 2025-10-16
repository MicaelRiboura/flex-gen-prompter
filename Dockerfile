FROM python:3.13-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala o uv
RUN pip install uv

# Configura uv para usar sempre o Python do sistema
ENV UV_NO_MANAGED_PYTHON=true
ENV UV_PYTHON_DOWNLOADS=never
ENV UV_NO_PYTHON_DOWNLOADS=true
ENV UV_LINK_MODE=copy

# Desabilita verificação de certificado se necessário
ENV UV_NO_VERIFY_SSL=true

WORKDIR /app

COPY pyproject.toml ./

# Instala as dependências do projeto usando uv
RUN uv sync

COPY . .