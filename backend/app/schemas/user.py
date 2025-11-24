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
    password: str
    
class UserUpdateName(BaseModel):
    name: str
    
class UserInDB(UserBase):
    id: UUID
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
