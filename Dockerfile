# Multi-stage build for a smaller image
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies (without BuildKit mount for compatibility)
COPY uv.lock pyproject.toml ./
RUN uv sync --frozen --no-install-project --no-dev

# Final stage
FROM python:3.14-slim

WORKDIR /app

# Install runtime dependencies (like bash for entrypoint)
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy the environment and uv binary from the builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv

# Add .venv/bin to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application code
COPY . .

# Set up environment variables
ENV DATABASE_URL=${DATABASE_URL}
ENV SERVER_TYPE=${SERVER_TYPE}

# Set up entrypoint for automated migrations
RUN chmod +x scripts/entrypoint.sh

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the API port
EXPOSE 8000

# Use the entrypoint script to run migrations then start supervisord
CMD ["./scripts/entrypoint.sh"]
