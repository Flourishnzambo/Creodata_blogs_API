from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    if not isinstance(password, str):
        raise ValueError("Password must be a string")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not isinstance(plain_password, str) or not isinstance(hashed_password, str):
        raise ValueError("Both plain_password and hashed_password must be strings")
    return pwd_context.verify(plain_password, hashed_password)