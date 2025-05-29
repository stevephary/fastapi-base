import datetime
from fastapi import HTTPException
from sqlmodel import Session, select

from app.core import security
from app.core.config import settings
from app.utils import Emailhandler
from app.user.models import User, Token, UserRegister, NewPassword

def get_user_by_email(*, session: Session, email: str) -> User | None:
    """Get user by email."""
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

def register_user(*, session: Session, user:UserRegister) -> None:
    """Register a new user."""
    db_user = get_user_by_email(session=session, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )
    hashed_password = security.get_password_hash(user.password)
    token = security.create_email_verification_token(user.email)
    verification_link = f"{settings.FRONTEND_HOST}/verify-email?token={token}"
    
    email_data = Emailhandler.generate_new_account_email(
        email_to=user.email,
        verification_link=verification_link
    )
    
    try:
        Emailhandler.send_email(
            email_to=user.email,
            subject=email_data.subject,
            html_content=email_data.html_content
        )
    except Exception as e:
        raise HTTPException(
            status_code=202,
            detail=f"Failed to send verification email: {str(e)}"
        )
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,
        is_verified=False,
    )
    
    session.add(db_user)
    session.commit()
    
def verify_user_email(*, session: Session, token: str) -> Token:
    """Verify user email."""
    email = security.verify_token(token=token)
    if not email:
        raise HTTPException(
            status_code=400,
            detail="Invalid token",
        )
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    if db_user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Email already verified",
        )
    db_user.is_verified = True
    db_user.updated_at = datetime.now()
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    access_token = security.create_access_token(
        subject=db_user.id,
        expires_delta=datetime.timedelta(hours=settings.ACCESS_TOKEN_EXPIRES_MINUTES)
    )
    token = Token(
        access_token=access_token,
        token_type="bearer",
    )
    return token

def resend_verification_email(*, session: Session, email: str) -> bool:
    """Resend verification email."""
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    if db_user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Email already verified",
        )
    token = security.create_email_verification_token(email=db_user.email)
    verification_link = f"{settings.FRONTEND_HOST}/verify-email?token={token}"
    
    email_data = Emailhandler.generate_new_account_email(
        email_to=db_user.email,
        verification_link=verification_link
    )
    
    try:
        Emailhandler.send_email(
            email_to=db_user.email,
            subject=email_data.subject,
            html_content=email_data.html_content
        )
    except Exception as e:
        raise HTTPException(
            status_code=202,
            detail=f"Failed to send verification email"
        )
    return True

def authenticate_user(*, session: Session, email: str, password: str) -> Token:
    """Authenticate user and return access token."""
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    if not security.verify_password(password, db_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
        )
  
    # if not db_user.is_verified:
    #     raise HTTPException(
    #         status_code=403,
    #         detail="Email not verified",
    #     )
    
    access_token = security.create_access_token(
        subject=db_user.id,
        expires_delta=datetime.timedelta(hours=settings.ACCESS_TOKEN_EXPIRES_MINUTES)
    )
    
    token = Token(
        access_token=access_token,
        token_type="bearer",
    )
    return token

def recover_password(*, session:Session, email:str) -> bool:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    
    token = security.generate_password_reset_token(email=email)
    email_data = Emailhandler.generate_reset_password_email(
        email_to=email,
        email=email,
        token=token,
    )
    
    Emailhandler.send_email(
        email_to= email,
        subject=email_data.subject,
        html_content=email_data.html_content,
        )
    return True

def reset_password(*, session:Session, new_password: NewPassword) -> bool:
    email = security.verify_token(token=new_password.token)
    if not email:
        raise HTTPException(
            status_code=400,
            detail="Invalid token",
        )
    
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    
    hashed_password = security.get_password_hash(new_password.password)
    db_user.hashed_password = hashed_password
    db_user.updated_at = datetime.now()
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return True
