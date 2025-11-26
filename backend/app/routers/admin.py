from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.database import get_db
from app.enums import UserRole
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserOut, ResponseModel
from app.utils.core.deps import get_current_staff
from app.utils.core.security import hash_password
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/create", dependencies=[Depends(get_current_staff)])
async def create_another_admin(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    existing = result.scalar_one_or_none()
    if existing:
        return error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Email already taken"
        )
        
    new_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hash_password(user.password),
        role=UserRole.ADMIN,
        email_verified=True
    )
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
            role=new_user.role,
            created_at=new_user.created_at
        )
    )
    
@router.put(
    "/user/{user_id}",
    response_model=ResponseModel[UserOut],
    dependencies=[Depends(get_current_staff)]
)
async def update_user(user_id: UUID, payload: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return error_response(
            message="User not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
        
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
        
    await db.commit()
    await db.refresh(user)
    
    return success_response(
        message="User updated successfully",
        data=UserOut.model_validate(user)
    )