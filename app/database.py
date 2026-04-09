import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Priority 1: Use DATABASE_URL if explicitly set
# Priority 2: Use SERVER_TYPE to determine default
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    SERVER_TYPE = os.getenv("SERVER_TYPE", "dev")
    if SERVER_TYPE == "production":
        # In production (Render), we expect the DATABASE_URL to be set
        # We fail early to avoid connecting to a default dev DB in prod
        raise ValueError("DATABASE_URL environment variable must be set when SERVER_TYPE is 'production'")
    else:
        # Default for local development
        DATABASE_URL = "postgresql://conneqtedagents:conneqtedagents@localhost:6543/traffic_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
