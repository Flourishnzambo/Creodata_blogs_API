from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class PostTagBase(BaseModel):
    post_id: int
    tag_ids: int

class PostTagCreate(PostTagBase):
    pass

class PostTagOut(PostTagBase):
    class Config:
        from_attributes = True