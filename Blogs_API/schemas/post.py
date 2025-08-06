from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from Blogs_API.schemas.tags import TagOut

class PostBase(BaseModel):
    title: str
    content: str
    category_id: int

class PostCreate(BaseModel):
    title: str
    content: str
    category_id: int
    created_by: int
    published_by: int
    tag_id: Optional[List[int]] = None

class PostUpdate(BaseModel):
    title: Optional[str]
    category_id: Optional[int]
    published_by: Optional[str]
    tag_id: Optional[List[int]] = None

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    category_id: int
    created_by: int
    published_by: int
    created_at: datetime
    published_at: datetime
    tags: List[TagOut] = []

    class Config:
        from_attributes = True

class PostOut(PostBase):
    id: int
    created_at: datetime
    published_at: datetime
    tags: List[TagOut]

    class Config:
      from_attributes = True



