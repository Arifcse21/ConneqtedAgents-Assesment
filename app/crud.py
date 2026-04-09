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

def clean_traffic_data(db: Session, keep_count: int = 5000):
    # Find the threshold record (the 5000th most recent)
    # We want to delete everything that comes AFTER the top 5000
    subquery = db.query(models.TrafficData.id).order_by(
        models.TrafficData.timestamp.desc(), 
        models.TrafficData.id.desc()
    ).offset(keep_count).limit(1).scalar()
    
    if subquery:
        # Get all IDs beyond the keep_count
        ids_to_delete = db.query(models.TrafficData.id).order_by(
            models.TrafficData.timestamp.desc(), 
            models.TrafficData.id.desc()
        ).offset(keep_count).all()
        
        if ids_to_delete:
            id_list = [r.id for r in ids_to_delete]
            db.query(models.TrafficData).filter(models.TrafficData.id.in_(id_list)).delete(synchronize_session=False)
            db.commit()
    
    return True
