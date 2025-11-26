from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.enums import UserRole

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, description="Must be at least 1 character long")
    
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Must be at least 8 characters")
    
class UserUpdateEmail(BaseModel):
    email: EmailStr
    
class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[UserRole] = None
    email_verified: Optional[bool] = None
    
class UserOut(UserBase):
    id: UUID
    email_verified: bool
    role: UserRole
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
