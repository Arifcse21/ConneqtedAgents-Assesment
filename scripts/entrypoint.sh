#!/bin/bash
set -e

# Run migrations if we're in any environment (dev/prod)
# This handles the free-tier Render limitation where pre-deploy is unavailable.
echo "Running database migrations..."
uv run alembic upgrade head

# Start the application
echo "Starting FastAPI application..."
exec uv run fastapi run main.py --port 8000
