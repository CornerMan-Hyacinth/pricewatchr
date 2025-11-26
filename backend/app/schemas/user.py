from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.enums import UserRole

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, description="Must be at least 1 character long")
    role: Optional[UserRole]
    
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Must be at least 8 characters")
    
class UserUpdateEmail(BaseModel):
    email: EmailStr
    
class UserUpdateName(BaseModel):
    name: str
    role: Optional[UserRole] = None
    
class UserOut(UserBase):
    id: UUID
    email_verified: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
