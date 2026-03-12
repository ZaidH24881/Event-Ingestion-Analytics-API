from pydantic import BaseModel
from typing import Optional, Dict, Any

class EventCreate(BaseModel):
    event_name: str
    user_id: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    project_id: str
    insert_id: Optional[str] = None