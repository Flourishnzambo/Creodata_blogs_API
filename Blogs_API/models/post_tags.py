from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.sql import func
from Blogs_API.database.database import Base
from Blogs_API.core import token  # Relative import


# Association table: post <-> tags
post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)
