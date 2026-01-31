from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    creator_type: str

    class Config:
        orm_mode = True
