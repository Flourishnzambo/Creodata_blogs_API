# create_tables.py

from Blogs.Blogs_API.database.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")
