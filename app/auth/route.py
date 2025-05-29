from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import service
from app.models import Message
from app.user.models import Token, UserRegister
from app.utils.deps import SessionDep

router = APIRouter(tags=["auth"])

@router.post("/register", status_code=201, response_model=Message)
def register_user(
    user:UserRegister,
    session: SessionDep,
) -> Message:
    """Register a new user."""
    service.register_user(session=session, user=user)
    return Message(message="User registered successfully. Please check your email to verify your account."
)
    
@router.post("/verify-email", status_code=200, response_model=Token)
def verify_email(
    token: str,
    session: SessionDep,
) -> Token:
    """Verify user email."""
    return service.verify_user_email(session=session, token=token)

@router.post("/resend-verification-email", status_code=200, response_model=Message)
def resend_verification_email(
    email: str,
    session: SessionDep,
) -> Message:
    """Resend verification email."""
    service.resend_verification_email(session=session, email=email)
    return Message(message="Verification email resent successfully.")

@router.post("/login", status_code=200, response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
) -> Token:
    """Login user and return access token."""
    return service.authenticate_user(session=session, email =form_data.username, password=form_data.password
)
    
@router.post("/recover-password", status_code=200, response_model=Message)
def recover_password(
    email: str,
    session: SessionDep,
) -> Message:
    """Recover user password."""
    service.recover_password(session=session, email=email)
    return Message(message="Password recovery email sent successfully.")

@router.post("/reset-password", status_code=200, response_model=Message)
def reset_password(
    token: str,
    new_password: str,
    session: SessionDep,
) -> Message:
    """Reset user password."""
    service.reset_password(session=session, token=token, new_password=new_password)
    return Message(message="Password reset successfully.")


