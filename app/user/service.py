from datetime import datetime
from uuid import UUID
from fastapi import HTTPException
from sqlmodel import Session,select
from app.core import security
from app.user.models import UpdatePassword, User, UserData



def get_user_by_id(*, session: Session, user_id: UUID) -> User | None:
    statement = select(User).where(User.id == user_id)
    session_user = session.exec(statement).first()
    return session_user

def get_current_user(*, session: Session, user_id: UUID) -> UserData:
    """Get current user by email."""
    db_user = get_user_by_id(session=session, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return UserData(email=db_user.email)

def update_password(*, session:Session, user_id: UUID, password:UpdatePassword) -> bool:
    user = get_user_by_id(session=session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not security.verify_password(password.current_password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect current password",
        )
    
    hashed_password = security.get_password_hash(password.new_password)
    user.hashed_password = hashed_password
    user.updated_at = datetime.now()
    session.add(user)
    session.commit()
    session.refresh(user)
    return True