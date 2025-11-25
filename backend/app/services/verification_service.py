import random
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from sqlalchemy.future import select
from uuid import UUID
from app.models import VerificationCode

async def create_verification_code(db: AsyncSession, user_id: UUID) -> str:
    # Generate 6-digit code
    code = f"{random.randint(0, 999999):06d}"
    
    # Expire in 10 minutes
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
    
    new_code = VerificationCode(
        user_id=user_id,
        code=code,
        expires_at=expires_at
    )
    db.add(new_code)
    await db.commit
    return code

async def verify_code(db: AsyncSession, user_id: UUID, code: str) -> bool:
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(VerificationCode)
        .where(VerificationCode.user_id == user_id)
        .where(VerificationCode.code == code)
        .where(VerificationCode.expires_at > now)
    )
    verification = result.scalar_one_or_none()
    
    if verification:
        # Delete after successful one-time use
        await db.execute(delete(VerificationCode).where(VerificationCode.id == verification.id))
        await db.commit()
        return True
    
    return False
