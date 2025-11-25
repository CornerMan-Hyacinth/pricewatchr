from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, List
from app.enums import ResponseStatus

T = TypeVar("T")

class ResponseModel(BaseModel, Generic[T]):
    status: ResponseStatus
    message: str
    data: Optional[T] = None
    
class ScrapedResult(BaseModel):
    product_id: str
    name: str
    scraped_prices: List[float]
    
class ScrapeAllResponse(BaseModel):
    status: ResponseStatus.SUCCESS
    count: int
    results: List[ScrapedResult]
    
class ScrapeProductResponse(BaseModel):
    status: ResponseStatus.SUCCESS
    product_id: str
    name: str
    scraped_prices: List[float]
    
