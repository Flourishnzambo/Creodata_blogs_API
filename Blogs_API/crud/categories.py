from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Blogs_API import models
from Blogs_API.models.users import User

from Blogs_API.models.categories import Category
from Blogs_API.models import categories as models
from Blogs_API.database.database import SessionLocal
from Blogs_API.schemas import categories
from Blogs_API.app.routers.aouth2 import get_current_user

router = APIRouter(prefix="/category", tags=["Categories"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Create a new category
@router.post("/", response_model=categories.CategoryOut)
def create_category(category: categories.CategoryCreate, db: Session = Depends(get_db)):
    new_category = models.Category(
       name=category.name,
       description=category.description,
       created_by=category.created_by,
       published_by=category.published_by
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Get all categories
@router.get("/", response_model=list[categories.CategoryOut])
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(models.Category).all()

#  Get one category by ID
@router.get("/{category_id}", response_model=categories.CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

#  Update a category (partial update)
@router.patch("/{category_id}", response_model=categories.CategoryOut)
def update_category(category_id: int, category_data: categories.CategoryUpdate, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for field, value in category_data.dict(exclude_unset=True).items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)
    return category

#  Delete a category
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"detail": "Category deleted successfully"}
