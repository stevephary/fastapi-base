from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session,select
from app.core import security
from app.user.models import UpdatePassword, User, UserData


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

def get_current_user(*, session: Session, user: str) -> UserData:
    """Get current user by email."""
    db_user = get_user_by_email(session=session, email=user)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return UserData(email=db_user.email)

def update_password(*, session:Session, email: str, password:UpdatePassword) -> bool:
    user = get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not security.verify_password(password.current_password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect current password",
        )
    
    hashed_password = security.get_password_hash(password.new_password)
    user.hashed_password = hashed_password
    user.updated_at = datetime.datetime.now()
    session.add(user)
    session.commit()
    session.refresh(user)
    return True