from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Blogs_API.database.database import Base
from Blogs_API.models.post_tags import post_tags
from Blogs_API.core import token  # Relative import



class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)

    posts = relationship("Post", secondary=post_tags, back_populates="tags")
