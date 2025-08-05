from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, Table, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Blogs_API.database.database import Base
from Blogs_API.core import token  # Relative import
from Blogs_API import schemas


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    published_by = Column(Integer, ForeignKey("users.id"))

    posts = relationship("Post", back_populates="category")
    creator = relationship("User", foreign_keys=[created_by])
    publisher = relationship("User", foreign_keys=[published_by])
