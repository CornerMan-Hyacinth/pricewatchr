from pydantic import BaseModel, Field
from typing import Literal

class AuthResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"

class EmailVerificationSendResponse(BaseModel):
    message: str
    detail: Literal["verification_code_sent"]

class EmailVerificationVerifyRequest(BaseModel):
    code: str  # 6-digit string like "813920"

class PasswordChangeRequest(BaseModel):
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8, description="Must be at least 8 characters")

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetConfirm(BaseModel):
    token: str = Field(..., description="Reset token from email")
    new_password: str = Field(..., min_length=8, description="Must be at least 8 characters")