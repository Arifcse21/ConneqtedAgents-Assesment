# Use a multi-stage build for a smaller image
FROM ghcr.io/astral-sh/uv:python3.14-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Final stage
FROM python:3.14-slim

WORKDIR /app

# Copy the environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Add .venv/bin to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application code
COPY . .

# Set dynamic environment logic
ENV SERVER_TYPE=prod

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the API port
EXPOSE 8000

# Start the application
CMD ["fastapi", "run", "main.py", "--port", "8000"]
