from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, Table, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Blogs_API.database.database import Base
from Blogs_API.models.post_tags import post_tags
from Blogs_API.core import token  # Relative import
from Blogs_API.models.tags import Tag 
from Blogs_API.models.users import User
from Blogs_API.models.categories import Category

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    content = Column(Text)
    published_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    published_by = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    created_by = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="posts", foreign_keys=[created_by])
    publisher = relationship("User", foreign_keys=[published_by])
    category = relationship("Category", back_populates="posts")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
