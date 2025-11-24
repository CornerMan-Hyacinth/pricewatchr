from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ProductUrlBase(BaseModel):
    product_id: UUID
    url: str
    is_primary: Optional[bool] = False
    retailer: Optional[str] = None
    
class ProductUrlCreate(ProductUrlBase):
    pass

class ProductUrlUpdate(BaseModel):
    url: Optional[str] = None
    is_primary: Optional[bool] = None
    retailer: Optional[str] = None

class ProductUrlInDB(ProductUrlBase):
    id: UUID

    model_config = {
        "from_attributes": True
    }
