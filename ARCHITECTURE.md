# System Architecture & Design Decisions

This document outlines the architectural choices and technical decisions made for the Smart City Traffic Monitoring System.

## 1. Core Technology Stack
- **Framework**: **FastAPI**
    - *Decision*: Chosen for its high performance, native asynchronous support, and automatic generation of interactive API documentation (Swagger). It is ideal for high-throughput data ingestion.
- **Database**: **PostgreSQL**
    - *Decision*: Provides ACID compliance, robust indexing for time-series data, and excellent support for concurrent writes. While SQLite was considered for simplicity, PostgreSQL is more reflective of a production environment.
- **ORM & Migrations**: **SQLAlchemy** & **Alembic**
    - *Decision*: SQLAlchemy provides a clean abstraction layer, and Alembic was integrated to ensure versioned, reproducible schema changes—a critical requirement for reliable DevOps pipelines.
- **Package Management**: **uv**
    - *Decision*: Used for extremely fast dependency installation and deterministic environments via `uv.lock`.

## 2. Infrastructure & Deployment
- **Containerization**: **Docker**
    - *Decision*: Used a **multi-stage build** to minimize the final image size (using `python:3.14-slim`) and improved security by running the application under a **non-root user**.
- **Process Management**: **Supervisord**
    - *Decision*: To satisfy the requirement for a separate ingestion process while staying within **Render's Free Tier** (one web service limit), `supervisord` is used to manage both the FastAPI server and the Ingestion Worker in a single container.
- **CI/CD**: **GitHub Actions**
    - *Decision*: Automated the build and deployment pipeline. Images are built and tagged on every push to `main`, and deployment is triggered on Render via a secure **webhook**.

## 3. Key Design Decisions
- **Dynamic Environment Logic**: Implemented a `SERVER_TYPE` (`dev`/`production`) strategy. The system automatically defaults to local Docker settings in `dev` but enforces explicit configuration in `production` to prevent accidental data leaks or misconnections.
- **Automated Startup Sequence**: Developed a custom `entrypoint.sh` that chains database migrations (`alembic upgrade head`) before starting the service. This ensures the database is always in sync without requiring a separate pre-deploy step (unsupported on Render Free Tier).
- **Capped Ingestion**: The ingestion worker is logic-aware; it checks the `/traffic/count` endpoint and pauses if the dataset exceeds 2000 records, protecting storage resources in a demo environment.

## 4. Scalability Strategy (1000+ req/s)
To handle future growth, the system is designed for:
1.  **Horizontal Scaling**: Stateless containers can be replicated behind a Load Balancer.
2.  **Ingestion Buffering**: Introducing a Message Queue (Kafka/RabbitMQ) between the ingestion endpoint and the database to handle spike loads.
3.  **Database Optimization**: Moving to **TimescaleDB** (Postgres extension) for specialized time-series optimizations and partition-based data pruning.
4.  **Read Replicas**: Utilizing PostgreSQL read replicas for the `GET /traffic` endpoints to offload traffic from the primary write node.
