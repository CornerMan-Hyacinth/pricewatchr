from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserOut, ResponseModel
from app.schemas.auth import (
    AuthResponse,
    EmailVerificationSendResponse,
    EmailVerificationVerifyRequest,
    PasswordChangeRequest,
    PasswordResetRequest,
    PasswordResetConfirm
)
from app.services.email_service import send_verification_email, send_password_reset_email
from app.services.verification_service import create_verification_code, verify_code
from app.services.password_reset_service import create_reset_token, validate_reset_token
from app.utils.core.security import hash_password, verify_password
from app.utils.core.auth import create_access_token
from app.utils.core.deps import get_current_user
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=ResponseModel[UserOut])
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    existing = result.scalar_one_or_none()
    if existing:
        return error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Email already taken"
        )
        
    new_user = User(email=user.email, name=user.name, hashed_password=hash_password(user.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="User created successfully",
        data=UserOut(
            id=new_user.id,
            email=new_user.email,
            name=new_user.name,
            created_at=new_user.created_at
        )
    )
    
@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form.password, user.hashed_password):
        return error_response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid credentials"
        )
        
    token = create_access_token({"sub": user.email})
    return AuthResponse(
        message="Logged in successfully",
        access_token=token
    )

#----------- Email verification -------------------------------
@router.post(
    "/email/verification/send",
    response_model=EmailVerificationSendResponse,
    status_code=status.HTTP_200_OK
)
async def send_verification_code(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.email_verified:
        return EmailVerificationSendResponse(
            message="Email already verified",
            detail="verification_code_sent"
        )
        
    code = await create_verification_code(db=db, user_id=current_user.id)
    background_tasks.addtask(send_verification_email, current_user.email, code, background_tasks)
    
    return EmailVerificationSendResponse(
        message="Verification code sent to your email",
        detail="verification_code_sent"
    )
    
@router.post(
    "/email/verification/verify",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK
)
async def verify_email_with_code(
    payload: EmailVerificationVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.email_verified:
        return error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Email already verified"
        )
        
    if not await verify_code(db=db, user_id=current_user.id, code=payload.code):
        return error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Invalid or expired verification code"
        )
        
    # Mark as verified
    current_user.email_verified = True
    await db.commit()
    
    # Return fresh token
    new_token = create_access_token({"sub": current_user.email})
    
    return AuthResponse(
        message="Email verified successfully",
        access_token=new_token
    )
    
#----------- Password flows ---------------------------------
# Change Password (Requires current password + session)
@router.post("/password/change")
async def change_password(
    payload: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not verify_password(payload.old_password, current_user.hashed_password):
        return error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Incorrect current password"
        )
        
    current_user.hashed_password = hash_password(payload.new_password)
    await db.commit()
    
    new_token = create_access_token({"sub": current_user.email})
    
    return AuthResponse(message="Password changed successfully", access_token=new_token)

# Request password reset
@router.post("/password/reset/request", response_model=ResponseModel[None])
async def send_reset_password_email(
    payload: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email.ilike(payload.email)))
    user = result.scalar_one_or_none()
    
    if user:
        reset_token = await create_reset_token(db=db, user_id=user.id)
        reset_link = f"https://pricewatchr.vercel.app/reset-password?token={reset_token}"
        
        background_tasks.add_task(
            send_password_reset_email,
            to=user.email,
            reset_link=reset_link,
            user_name=user.name or "User"
        )
        
    return success_response(message="If the email exists, a reset link has been sent")

# Confirm password reset (token-based)
@router.post("/password/reset/confirm", response_model=AuthResponse)
async def reset_password(payload: PasswordResetConfirm, db: AsyncSession = Depends(get_db)):
    user_id = await validate_reset_token(db, payload.token)
    if not user_id:
        return error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Invalid or expired reset token"
        )
        
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one()
    
    user.hashed_password = hash_password(payload.new_password)
    await db.commit()
    
    new_token = create_access_token({"sub": user.email})
    
    return AuthResponse(
        message="Password reset successfully",
        access_token=new_token
    )
