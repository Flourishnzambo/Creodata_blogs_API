from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Blogs_API import models
from Blogs_API.models import post as models
from Blogs_API.database.database import SessionLocal
from typing import List
from Blogs_API.schemas import post_tags
from Blogs_API.models.post_tags import post_tags
from Blogs_API.schemas import post_tags
from Blogs_API.app.routers.aouth2 import get_current_user
from Blogs_API.models.users import User

router = APIRouter(prefix="/post_tags", tags=["Post Tags"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create post-tag relationship
@router.post("/{post_id}/tags")
def assign_tags(post_id: int, tag_ids: List[int], db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    for tag_id in tag_ids:
        tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
        if not tag:
            continue  # or raise 404

        exists = db.execute(
            models.post_tags.select().where(
                (models.post_tags.c.post_id == post_id) &
                (models.post_tags.c.tag_id == tag_id)
            )
        ).first()

        if not exists:
            db.execute(models.post_tags.insert().values(post_id=post_id, tag_id=tag_id))

    db.commit()
    return {"message": "Tags assigned"}

# Get all tags for a post
@router.get("/post_tags/{post_id}", response_model=List[post_tags.PostTagOut])
def get_tags_for_post(post_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post.tags

# Remove a tag from a post
@router.delete("/posts/{post_id}/post_tags/{tag_id}", status_code=204)
def remove_tag_from_post_by_url(post_id: int, tag_id: int, db: Session = Depends(get_db),
                                current_user: User = Depends(get_current_user)):
    stmt = models.post_tags.delete().where(
        (models.post_tags.c.post_id == post_id) &
        (models.post_tags.c.tag_id == tag_id)
    )
    result = db.execute(stmt)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tag relation not found")

