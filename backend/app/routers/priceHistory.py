from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import crud
from app.database import get_db
from app.schemas import PriceHistoryInDB, PriceHistoryCreate, ResponseModel
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/price-history", tags=["Price History"])

@router.post("/", response_model=ResponseModel[PriceHistoryInDB], status_code=status.HTTP_201_CREATED)
async def create_price_history(data: PriceHistoryCreate, db: AsyncSession = Depends(get_db)):
    new_price_history = await crud.create_price_history(db=db, data=data)
    return success_response(
        message="Price history record created successfully.",
        data=new_price_history,
        status_code=status.HTTP_201_CREATED
    )
    
@router.get("/product/{product_id}", response_model=ResponseModel[List[PriceHistoryInDB]])
async def get_price_history_by_product(product_id: str, db: AsyncSession = Depends(get_db)):
    price_history_records = await crud.get_price_history_by_product(db=db, product_id=product_id)
    return success_response(
        message="Price history records retrieved successfully.",
        data=price_history_records
    )
    
@router.get("/{ph_id}", response_model=ResponseModel[PriceHistoryInDB])
async def get_price_history(ph_id: str, db: AsyncSession = Depends(get_db)):
    price_history = await crud.get_price_history_by_id(db=db, ph_id=ph_id)
    if not price_history:
        return error_response(
            message="Price history record not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(
        message="Price history record retrieved successfully.",
        data=price_history
    )
    
@router.delete("/{ph_id}", response_model=ResponseModel[None])
async def delete_price_history(ph_id: str, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_price_history(db=db, ph_id=ph_id)
    if not deleted:
        return error_response(
            message="Price history record not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(
        message="Price history record deleted successfully.",
        data=None
    )