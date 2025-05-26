import jwt
from pydantic import ValidationError
from app.core.config import settings
from app.core.db import engine
from jwt.exceptions import InvalidTokenError
from fastapi import status
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from typing import Annotated, Generator
from typing_extensions import Self

from app.core.security import ALGORITHM
from app.user.models import TokenPayload, User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(session: SessionDep ,token: TokenDep) -> User:
    try:
       payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
       token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]