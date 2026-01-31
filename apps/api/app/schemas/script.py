from pydantic import BaseModel
from typing import Optional, Dict, Any

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
