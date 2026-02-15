from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ScriptUpdate(BaseModel):
    status: str
    performance_data: Optional[Dict[str, Any]] = None

class ScriptResponse(BaseModel):
    id: int
    user_id: int
    topic: str
    script_json: Dict[str, Any]
    status: str
    performance_data: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True

class ScriptListResponse(BaseModel):
    id: int
    user_id: int
    topic: str
    status: str
    hook: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
