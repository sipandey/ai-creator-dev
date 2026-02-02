from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class GenerateScriptRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200, description="The topic for the script")

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
