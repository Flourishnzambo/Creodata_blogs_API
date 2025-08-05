from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Blogs_API import models
from Blogs_API.database.database import SessionLocal
import Blogs_API.schemas.tags as tags_schemas
from Blogs_API.models.users import User
import Blogs_API.models.tags as tags_models
from Blogs_API.models import tags as models
from Blogs_API.app.routers.aouth2 import get_current_user

router = APIRouter(prefix="/tags", tags=["Tags"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE a tag
@router.post("/", response_model=tags_schemas.TagOut)
def create_tag(tag: tags_schemas.TagCreate, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    db_tag = db.query(tags_models.Tag).filter(tags_models.Tag.name == tag.name).first()
    if db_tag:
        raise HTTPException(status_code=400, detail="Tag already exists")
    new_tag = models.Tag(name=tag.name)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag

# READ all tags
@router.get("/", response_model=list[tags_schemas.TagOut])
def get_all_tags(db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    return db.query(tags_models.Tag).all()

# READ one tag by ID
@router.get("/{tag_id}", response_model=tags_schemas.TagOut)
def get_tag(tag_id: int, db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)):
    tag = db.query(tags_models.Tag).filter(tags_models.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

# UPDATE tag
@router.patch("/{tag_id}", response_model=tags_schemas.TagOut)
def update_tag(tag_id: int, updated_tag: tags_schemas.TagCreate, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    tag = db.query(tags_models.Tag).filter(tags_models.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag.name = updated_tag.name
    db.commit()
    db.refresh(tag)
    return tag

# DELETE tag
@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    tag = db.query(tags_models.Tag).filter(tags_models.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    db.commit()
    return {"detail": "Tag deleted successfully"}
