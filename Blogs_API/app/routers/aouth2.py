# this code checks if the user i authenticated for loging in

from jose import JWTError, jwt #Helps us decode and validate JWT tokens (like a passport for API users)
from fastapi import Depends, HTTPException, status #Allows us to define dependencies and handdle errors with HTTP status codes
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from Blogs_API.database.database import get_db
from Blogs_API.models import users as models
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Get your secret key & algorithm
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  

# Get user ID from token
def verify_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = int(payload.get("user_id"))
        exp = payload.get("exp")

        if user_id is None:
            raise credentials_exception
        return int(user_id)
    except JWTError:
        raise credentials_exception

# Get the current user from the DB using the user_id from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_access_token(token)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
