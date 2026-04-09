from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TrafficDataBase(BaseModel):
    location_id: str
    vehicle_count: int
    average_speed: float
    congestion_level: str  # low / medium / high

class TrafficDataCreate(TrafficDataBase):
    timestamp: Optional[datetime] = None

class TrafficData(TrafficDataBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class CleanRequest(BaseModel):
    command: str
