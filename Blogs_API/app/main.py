from fastapi import FastAPI
from Blogs_API.crud import categories, post, post_tags, tags, users
from Blogs_API.database.database import Base, engine
from Blogs_API.app.routers import auth


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(post.router)
app.include_router(tags.router)
app.include_router(categories.router)
app.include_router(post_tags.router)
app.include_router(auth.router)
