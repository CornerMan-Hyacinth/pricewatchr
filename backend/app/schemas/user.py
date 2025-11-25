from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str
    
class UserCreate(UserBase):
    password: str
    
class UserUpdateEmail(BaseModel):
    email: EmailStr
    
class UserUpdateName(BaseModel):
    name: str
    
class UserOut(UserBase):
    id: UUID
    email_verified: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
