from pydantic import BaseModel
from typing import Literal

class EmailVerificationSendResponse(BaseModel):
    message: str
    detail: Literal["verification_code_sent"]

class EmailVerificationVerifyRequest(BaseModel):
    code: str  # 6-digit string like "813920"

class AuthResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"