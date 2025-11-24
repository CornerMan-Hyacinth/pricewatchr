from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PriceHistoryBase(BaseModel):
    product_id: UUID
    product_url_id: UUID
    recorded_at: datetime
    price: float
    
class PriceHistoryCreate(PriceHistoryBase):
    pass

class PriceHistoryInDB(PriceHistoryBase):
    id: UUID

    model_config = {
        "from_attributes": True
    }
