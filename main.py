from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.database import SessionLocal, engine

# Note: Table creation is now handled by Alembic migrations.
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart City Traffic Monitoring System")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Smart City Traffic Monitoring System",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/traffic", response_model=schemas.TrafficData)
def create_traffic(traffic_data: schemas.TrafficDataCreate, db: Session = Depends(get_db)):
    return crud.create_traffic_data(db=db, traffic_data=traffic_data)

@app.get("/traffic", response_model=List[schemas.TrafficData])
def read_traffic(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_traffic_data(db, skip=skip, limit=limit)

@app.get("/traffic/count")
def read_traffic_count(db: Session = Depends(get_db)):
    count = crud.get_traffic_count(db)
    return {"count": count}
