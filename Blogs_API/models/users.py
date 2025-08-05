from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, Table, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Blogs_API.database.database import Base
from Blogs_API.core import token  # Relative import


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    role = Column(String(50), default="user")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    posts = relationship("Post", back_populates="creator", foreign_keys="Post.created_by")
    # published_posts = relationship("Post", foreign_keys="Post.published_by")  # optional