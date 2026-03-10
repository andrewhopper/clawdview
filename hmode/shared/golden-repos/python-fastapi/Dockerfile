# syntax=docker/dockerfile:1
FROM python:3.11-slim as base

# Prevent Python from writing bytecode and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv for fast dependency management
RUN pip install uv

# --- Dependencies stage ---
FROM base as deps

COPY pyproject.toml ./
RUN uv pip install --system -e .

# --- Development stage ---
FROM deps as dev

COPY pyproject.toml ./
RUN uv pip install --system -e ".[dev]"

COPY . .

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# --- Production stage ---
FROM base as prod

# Create non-root user
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser

COPY pyproject.toml ./
RUN uv pip install --system -e .

COPY --chown=appuser:appgroup . .

USER appuser

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
