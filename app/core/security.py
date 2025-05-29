import datetime
from typing import Any, Optional
import jwt
import uuid
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: datetime.timedelta) -> str:
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_email_verification_token(email: str) -> str:
    delta = datetime.timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRES_MINUTES)
    now = datetime.datetime.now(datetime.timezone.utc)
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def generate_password_reset_token(email: str) -> str:
    delta = datetime.timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
    now = datetime.datetime.now(datetime.timezone.utc)
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def verify_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        return str(decoded_token["sub"])
    except jwt.InvalidTokenError:
        return None
    
    

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)