# src/models/notification_models.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: str
    title: str  
    type: str   
    message: str
    priority: str = "MEDIUM"  
    metadata: Optional[Dict[str, Any]] = {}

class Notification(NotificationCreate):
    id: str                 # <--- Importante: que se llame 'id'
    created_at: datetime
    read: bool = False      # <--- Importante: que se llame 'read'