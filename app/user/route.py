from fastapi import APIRouter, Depends
from app.models import Message
from app.user.models import UpdatePassword, UserData
from app.utils.deps import CurrentUser, SessionDep
from app.user import service

router = APIRouter(tags=["user"])

@router.put("/update-password", status_code=200, response_model=Message)
def update_password(
    password: UpdatePassword,
    current_user: CurrentUser,
    session: SessionDep
) -> Message:
    """Update user password."""
    service.update_password(session=session, user_id=current_user.id, password=password)
    return Message(message="Password updated successfully.")

@router.get("/me", status_code=200, response_model=UserData)
def get_current_user_data(
    current_user: CurrentUser,
    session: SessionDep
) -> UserData:
    """Get current user data."""
    return service.get_current_user(session=session, user_id=current_user.id)


