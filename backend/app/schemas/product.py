from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    target_price: Optional[float] = None
    
class ProductCreate(ProductBase):
    urls: List[str] = Field(..., min_items=1)
    primary_url: Optional[int] = 0  # index of the primary url in the urls list
    retailers: List[Optional[str]] = None
    
    @field_validator("primary_url")
    def validate_primary_url(cls, v: Optional[int], info: ValidationInfo) -> int:
        urls: List[str] = info.data.get("urls", [])
        if v is not None and (v < 0 or v >= len(urls)):
            raise ValueError(f"primary_url {v} out of range (urls has {len(urls)} items)")
        return v if v is not None else 0
    
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    target_price: Optional[float] = None
    current_price: Optional[float] = None
    
class ProductInDB(ProductBase):
    id: UUID
    user_id: UUID
    current_price: Optional[float] = None
    last_checked: Optional[datetime] = None
    added_at: datetime

    model_config = {
        "from_attributes": True
    }
