from pydantic import BaseModel
from typing import Optional



class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    created_by: int
    published_by: int

class CategoryOut(CategoryBase):
    id: int
   
    class Config:
        from_attributes = True
        
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    published_by: Optional[int] = None