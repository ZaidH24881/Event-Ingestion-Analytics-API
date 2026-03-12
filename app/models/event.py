"""Event model for tracking user interactions"""
from ..core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, JSON, Index
from sqlalchemy.sql import func

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    insert_id = Column(String, unique=True, index=True)  # idempotency
    event_name = Column(String, index=True)
    timestamp = Column(DateTime, default=func.now(), index=True)
    user_id = Column(String, nullable=True)
    properties = Column(JSON, nullable=True)  # flexible event data
    project_id = Column(String, nullable=True)