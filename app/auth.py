from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC

from app.settings import settings

SECRET_KEY = settings.secret_key
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in the environment variables.")
ALGORITHM = settings.algorithm or "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes or 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
