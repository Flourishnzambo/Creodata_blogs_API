# routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from Blogs_API.database.database import get_db
from Blogs_API.models import users as models
from Blogs_API.core.token import create_access_token
from Blogs_API.core.security import verify_password  # if you use password hashing

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Step 1: Fetch the user
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Step 2: Generate token using user.id
    access_token = create_access_token(user_id=user.id)

    # Step 3: Return the token
    return {"access_token": access_token, "token_type": "bearer"}
