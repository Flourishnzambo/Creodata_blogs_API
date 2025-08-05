from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = None

class TagOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True
