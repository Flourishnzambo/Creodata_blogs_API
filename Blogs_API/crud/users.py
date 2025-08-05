# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Blogs_API.core.security import hash_password
from ..database.database import SessionLocal
import Blogs_API.schemas.users as user_schemas
import Blogs_API.models.users as user_models
from Blogs_API.models.users import User
from Blogs_API.app.routers.aouth2 import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Create a new user
@router.post("/", response_model=user_schemas.UserOut)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    db_user = db.query(user_models.User).filter(user_models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = user_models.User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
        phone_number=user.phone_number
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get all users
@router.get("/", response_model=list[user_schemas.UserOut])
def get_all_users(db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    return db.query(user_models.User).all()

# Get user by ID
@router.get("/{user_id}", response_model=user_schemas.UserOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(user_models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user (partial)
@router.patch("/{user_id}", response_model=user_schemas.UserOut)
def update_user(user_id: int, updated_data: user_schemas.UserUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    user = db.query(user_models.User).filter(user_models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    #  allow username update
    if updated_data.email is not None:
        user.email = updated_data.email
    if updated_data.role is not None:
        user.role = updated_data.role
    if updated_data.password is not None:
        user.password_hash = hash_password(updated_data.password)
    if updated_data.password is not None:
       user.phone_number = updated_data.phone_number
    db.commit()
    db.refresh(user)

    return user

# Delete a user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    user = db.query(user_models.User).filter(user_models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": f"User with id {user_id} deleted successfully"}


