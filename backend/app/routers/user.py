from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models import User
from app.schemas import UserUpdateEmail, UserUpdateName, UserOut, ResponseModel
from app.utils.core.auth import create_access_token
from app.utils.core.deps import get_current_user
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/me", tags=["Profile"])

@router.get("/", response_model=ResponseModel[UserOut])
async def get_profile(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(User).where(User.id == current_user.id))
    user = result.scalar_one_or_none()
    if not user:
        return error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message="User not found"
        )
        
    return success_response(
        message="User retrieved successfully",
        data=UserOut(id=user.id, email=user.email, name=user.name, created_at=user.created_at)
    )
    
@router.patch("/email", response_model=ResponseModel[dict])
async def change_email(
    data: UserUpdateEmail,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if email is already in use
    if data.email.lower() != current_user.email.lower():
        result = await db.execute(select(User).where(User.email == data.email))
        if result.scalar_one_or_none():
            return error_response(
                status_code=status.HTTP_409_CONFLICT,
                message="This email is already in use"
            )
        
    # Update the user
    current_user.email = data.email.lower()
    
    await db.commit()
    
    # Generate new access token with updated sub
    new_token = create_access_token({"sub": current_user.email})
    
    return success_response(
        message="Email changed successfully",
        data={
            "user": UserOut.model_validate(current_user),
            "access_token": new_token,
            "token_type": "bearer"
        }
    )
    
@router.patch("/name", response_model=ResponseModel[UserOut])
async def change_name(
    data: UserUpdateName,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.name = data.name
    await db.commit()
    
    return success_response(
        message="Name changed successfully",
        data=UserOut.model_validate(current_user)
    )
