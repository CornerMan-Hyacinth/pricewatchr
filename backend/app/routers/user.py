from fastapi import APIRouter, Depends, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models import User
from app.schemas import UserUpdateEmail, UserUpdate, UserOut, ResponseModel
from app.utils.core.auth import create_access_token
from app.utils.core.deps import get_current_user
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/users", tags=["Profile"])

@router.get("/me", response_model=ResponseModel[UserOut])
async def get_profile(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return success_response(
        message="User retrieved successfully",
        data=UserOut(current_user)
    )
    
@router.patch("/me", response_model=ResponseModel[UserOut])
async def update_user(
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)
        
    await db.commit()
    await db.refresh(current_user)
    
    return success_response(
        message="Name changed successfully",
        data=UserOut.model_validate(current_user)
    )
    
@router.patch("/me/email", response_model=ResponseModel[dict])
async def update_user_email(
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

@router.delete("/me", response_model=ResponseModel[None], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    await db.execute(delete(User).where(User.id == current_user.id))
    await db.commit()
    
    return success_response(
        status_code=status.HTTP_204_NO_CONTENT,
        message="User deleted successfully"
    )
