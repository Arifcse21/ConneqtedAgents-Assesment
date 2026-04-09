# Smart City Traffic Monitoring System

This is a FastAPI-based backend service designed to ingest and monitor real-time traffic data for a smart city.

## Features
- **Data Ingestion**: Near real-time ingestion via `POST /traffic`.
- **Data Retrieval**: Recent traffic data access via `GET /traffic`.
- **Health Check**: Service status monitoring via `/health`.
- **Dockerized**: Multi-stage build for optimized production deployment.
- **CI/CD**: Automated testing, building, and deployment via GitHub Actions.

### Environment Variables
- `SERVER_TYPE`: Set to `dev` for local development (defaults to local Docker DB) or `prod` for production (requires `DATABASE_URL`).
- `DATABASE_URL`: Explicit connection string. If provided, it overrides `SERVER_TYPE` defaults.

## Setup Instructions

### 1. Database Setup (PostgreSQL)
Run the following command to start a PostgreSQL instance with the required configuration:

```bash
docker run --name traffic-db \
  --restart=unless-stopped \
  -e POSTGRES_USER=conneqtedagents \
  -e POSTGRES_PASSWORD=conneqtedagents \
  -e POSTGRES_DB=traffic_db \
  -p 6543:5432 \
  -d postgres
```

### 2. Database Migrations
Before starting the application, apply the database migrations:

```bash
DATABASE_URL=postgresql://conneqtedagents:conneqtedagents@localhost:6543/traffic_db uv run alembic upgrade head
```

### 3. Local Development (Running the API)
Install dependencies and run the server in development mode:

```bash
# Install dependencies
uv sync

# Run the FastAPI server (Development)
uv run fastapi dev main.py

# Run the FastAPI server (Production mode)
uv run fastapi run main.py
```

### 4. Data Ingestion Simulation
Run the ingestion script in a separate terminal to start generating simulated traffic data:

```bash
uv run scripts/ingest_data.py
```

## Architecture Decisions & Trade-offs

### Database: PostgreSQL
- **Why**: Chosen for its robustness, ACID compliance, and strong support for concurrent writes. While SQLite is simpler for local demos, PostgreSQL is the standard for production-grade reliability.
- **Trade-offs**: Slightly more overhead than NoSQL for simple data structures, but provides better consistency and querying power for structured traffic metrics.

### Framework: FastAPI
- **Why**: High performance (async support), automatic Swagger documentation (`/docs`), and type safety via Pydantic.
- **Trade-offs**: Requires an ASGI server like Uvicorn, but the performance benefits for high-throughput ingestion are worth it.

## Scalability Considerations

### Future-Proofing for 1000+ Requests/Second
1.  **Horizontal Scaling**: Deploy multiple instances of the FastAPI service behind a load balancer (Nginx/HAProxy).
2.  **Message Queue**: Introduce Kafka or RabbitMQ between the Ingestion API and the Database. This "buffers" the bursts of traffic and allows the database to process writes at a steady rate.
3.  **Database Partitioning**: Use table partitioning in PostgreSQL (by `timestamp`) or move to a dedicated Time-Series database like **TimescaleDB** or **InfluxDB** for efficient storage of high-frequency data.
4.  **Caching**: Use Redis to cache the most recent/frequent traffic queries for `GET /traffic`.

## Deployment
This application is configured for deployment on **Render** via GitHub Actions.
- Pipeline: Push to `main` -> Docker Build -> Trigger Render Deploy Hook.

## API Documentation
Once running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

### Key Endpoints:
- `GET /`: Root info.
- `GET /health`: Health check.
- `POST /traffic`: Ingest data.
- `GET /traffic`: Fetch recent data.
- `GET /traffic/count`: Total record count.
- `POST /clean`: Truncates dataset. Requires `{ "command": "sudo" }` in the request body.

## Production: on RENDER swagger URL
[https://conneqtedagents-assesment.onrender.com/docs](https://conneqtedagents-assesment.onrender.com/docs)