#!/bin/bash
set -e

# Run migrations if we're in any environment (dev/prod)
# This handles the free-tier Render limitation where pre-deploy is unavailable.
echo "Running database migrations..."
uv run alembic upgrade head

# Start the application manager (supervisord)
echo "Starting multi-process manager (supervisord)..."
exec uv run supervisord -c supervisord.conf
