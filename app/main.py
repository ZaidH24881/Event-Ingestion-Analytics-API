from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .core.database import Base, engine, dependency_db_session
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from .models.event import Event
from .api.routes.event import EventCreate
from datetime import datetime
import uuid

app = FastAPI(title="Event Analytics API")

# enable CORS for browser-based demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create database tables
Base.metadata.create_all(bind=engine)

@app.post("/track")
def track_event(
    event_data: EventCreate, 
    db: Session = Depends(dependency_db_session)
):
    """Track an event with automatic idempotency via insert_id"""
    
    # create id 
    if not event_data.insert_id:
        event_data.insert_id = str(uuid.uuid4())
    
    # Create event instance
    event_instance = Event(
        event_name=event_data.event_name,
        user_id=event_data.user_id,
        properties=event_data.properties,
        project_id=event_data.project_id,
        insert_id=event_data.insert_id
    )
    
    try:
        db.add(event_instance)
        db.commit()
        db.refresh(event_instance)
        return {"message": "Event tracked successfully", "event_id": event_instance.id}
    except IntegrityError:
        # duplicate insert_id,  idempotency at work
        db.rollback()
        return {"message": "Event already tracked (duplicate insert_id)", "status": "ignored"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/metrics/dau") 
def get_dau(
    start_date: str, 
    end_date: str,
    db: Session = Depends(dependency_db_session)
):
    """Get Daily Active Users - uses database aggregation for performance"""
    
    try:
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)."
        )
    
    results = (
        db.query(
            func.date(Event.timestamp).label('date'),
            func.count(func.distinct(Event.user_id)).label('dau')
        )
        .filter(Event.timestamp >= start_dt, Event.timestamp <= end_dt)
        .filter(Event.user_id.isnot(None))
        .group_by(func.date(Event.timestamp))
        .all()
    )
    
    return {str(row.date): row.dau for row in results}

