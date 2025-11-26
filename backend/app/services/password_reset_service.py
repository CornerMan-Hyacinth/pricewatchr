import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.models import PasswordResetToken

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

async def create_reset_token(db: AsyncSession, user_id: UUID) -> str:
    raw_token = secrets.token_urlsafe(32)
    token_hash = hash_token(raw_token)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    
    reset_token = PasswordResetToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at
    )
    db.add(reset_token)
    await db.commit()
    
    return raw_token # <- send this to the email, don't store it

async def validate_reset_token(db: AsyncSession, token: str) -> UUID | None:
    token_hash = hash_token(token)
    now = datetime.now(timezone.utc)
    
    result = await db.execute(
        select(PasswordResetToken)
        .where(PasswordResetToken.token_hash == token_hash)
        .where(PasswordResetToken.expires_at > now)
    )
    db_token = result.scalar_one_or_none()
    if not db_token:
        return None
    
    # Delete immediately after use
    await db.execute(delete(PasswordResetToken).where(PasswordResetToken.id == db_token.id))
    await db.commit()
    
    return db_token.user_id
