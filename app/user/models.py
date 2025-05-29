import uuid
from datetime import datetime
from pydantic import EmailStr
from sqlalchemy import String
from sqlmodel import Field, SQLModel

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255, sa_type=String(255) )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=True)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    
class UserRegister(SQLModel):
    email: EmailStr | None = Field(default=None)
    password: str| None = Field(default=None, min_length=6, max_length=128)
    
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None)
    password: str | None = Field(default=None, min_length=6, max_length=128)

class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=6, max_length=128)
    new_password: str = Field(min_length=6, max_length=128)

class NewPassword(SQLModel):
    password: str = Field(min_length=6, max_length=128)
    token: str 
    
class UserData(SQLModel):
    email: EmailStr
    
class Token(SQLModel):
    access_token: str
    token_type: str = Field(default="bearer")
    
class RefreshToken(SQLModel):
    refresh_token: str
    token_type: str = Field(default="bearer")
    
class TokenPayload(SQLModel):
    sub: str
    
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(
        max_length=128, sa_type=String(128), nullable=False
    )  
    __tablename__ = "users"
    

    