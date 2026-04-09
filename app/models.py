from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base
import datetime

class TrafficData(Base):
    __tablename__ = "traffic_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    location_id = Column(String, index=True)
    vehicle_count = Column(Integer)
    average_speed = Column(Float)
    congestion_level = Column(String)  # low / medium / high
