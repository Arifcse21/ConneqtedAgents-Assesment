from sqlalchemy.orm import Session
from . import models, schemas
import datetime

def get_traffic_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TrafficData).order_by(models.TrafficData.timestamp.desc()).offset(skip).limit(limit).all()

def create_traffic_data(db: Session, traffic_data: schemas.TrafficDataCreate):
    db_traffic = models.TrafficData(
        location_id=traffic_data.location_id,
        vehicle_count=traffic_data.vehicle_count,
        average_speed=traffic_data.average_speed,
        congestion_level=traffic_data.congestion_level,
        timestamp=traffic_data.timestamp or datetime.datetime.utcnow()
    )
    db.add(db_traffic)
    db.commit()
    db.refresh(db_traffic)
    return db_traffic

def get_traffic_count(db: Session):
    return db.query(models.TrafficData).count()

def clean_traffic_data(db: Session):
    db.query(models.TrafficData).delete()
    db.commit()
    return True
