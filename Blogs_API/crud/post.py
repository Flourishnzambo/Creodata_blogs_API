from fastapi import APIRouter,UploadFile,File, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from Blogs_API import models
from ..database.database import get_db
from Blogs_API.schemas.token import TokenData
from Blogs_API.app.routers.aouth2 import get_current_user
import fitz 
from typing import Optional, List
from Blogs_API.models.post import Post
from Blogs_API.models.tags import Tag
from Blogs_API.schemas.post import PostOut, PostCreate, PostResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



router = APIRouter(prefix="/posts", tags=["Posts"])


# CREATE POST
@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db)
):
    

    db_post = Post(
        title=post_data.title,
        content=post_data.content,
        category_id=post_data.category_id,
        created_by=post_data.created_by,
        published_by=post_data.published_by
    )

    if post_data.tag_id:
        tags = db.query(Tag).filter(Tag.id.in_(post_data.tag_id)).all()
        db_post.tags = tags

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post



# GET ALL POSTS
@router.get("/", response_model=List[PostResponse])
def get_all_posts(
    db: Session = Depends(get_db),
    current_user: models.users = Depends(get_current_user)  
):
    logger.info(f"Authenticated user: {current_user.email}")
    print("Fetching posts...")

    posts = db.query(Post).all()
    print(f"Found {len(posts)} posts.")

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found"
        )

    return posts



# GET ONE POST BY ID
@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.users = Depends(get_current_user)
):
    """Get a specific post - requires authentication"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} not found"
        )
    
    return post

# UPDATE POST
@router.patch("/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    title: Optional[str] = None,
    category_id: Optional[int] = None,
    published_by: Optional[str] = None,
    tag_id: Optional[List[int]] = None,
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.users = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if title:
        post.title = title
    if category_id:
        post.category_id = category_id
    if published_by:
        post.published_by = published_by
    if tag_id:
        tags = db.query(Tag).filter(Tag.id.in_(tag_id)).all()
        post.tags = tags

    if file:
        if file.content_type not in ["application/pdf", "text/plain"]:
            raise HTTPException(status_code=415, detail="Only PDF and TXT files are allowed")

        try:
            contents = file.file.read()
            if file.content_type == "application/pdf":
                doc = fitz.open(stream=contents, filetype="pdf")
                full_text = ""
                for page in doc:
                    full_text += page.get_text()
                doc.close()
            elif file.content_type == "text/plain":
                full_text = contents.decode("utf-8")
            else:
                raise HTTPException(status_code=415, detail="Unsupported file type")

            post.content = full_text

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

    db.commit()
    db.refresh(post)
    return post

# DELETE POST
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), 
                current_user: models.users = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
