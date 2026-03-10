# syntax=docker/dockerfile:1
FROM python:3.11-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

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

CMD ["python", "-m", "mylib"]

# --- Production stage ---
FROM base as prod

RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser

COPY pyproject.toml ./
RUN uv pip install --system -e .

COPY --chown=appuser:appgroup . .

USER appuser

CMD ["python", "-m", "mylib"]
