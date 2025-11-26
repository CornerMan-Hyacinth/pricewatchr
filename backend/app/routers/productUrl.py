from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import crud
from app.database import get_db
from app.schemas import ProductUrlInDB, ProductUrlCreate, ProductUrlUpdate, ResponseModel
from app.utils.core.deps import get_current_user
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/product-urls", tags=["Product Urls"])

@router.post(
    "/",
    response_model=ResponseModel[ProductUrlInDB],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)]
)
async def create_product_url(data: ProductUrlCreate, db: AsyncSession = Depends(get_db)):
    new_product_url = await crud.create_product_url(db=db, data=data)
    return success_response(
        message="Product URL created successfully.",
        data=new_product_url,
        status_code=status.HTTP_201_CREATED
    )
    
@router.get(
    "/product/{product_id}",
    response_model=ResponseModel[List[ProductUrlInDB]],
    dependencies=[Depends(get_current_user)]
)
async def get_product_urls_by_product(product_id: str, db: AsyncSession = Depends(get_db)):
    product_urls = await crud.get_product_urls_by_product(db=db, product_id=product_id)
    return success_response(
        message="Product URLs retrieved successfully.",
        data=product_urls
    )
    
@router.get(
    "/{pu_id}",
    response_model=ResponseModel[ProductUrlInDB],
    dependencies=[Depends(get_current_user)]
)
async def get_product_url(pu_id: str, db: AsyncSession = Depends(get_db)):
    product_url = await crud.get_product_url_by_id(db=db, pu_id=pu_id)
    if not product_url:
        return error_response(
            message="Product URL not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(
        message="Product URL retrieved successfully.",
        data=product_url
    )
    
@router.put(
    "/{pu_id}",
    response_model=ResponseModel[ProductUrlInDB],
    dependencies=[Depends(get_current_user)]
)
async def update_product_url(pu_id: str, data: ProductUrlUpdate, db: AsyncSession = Depends(get_db)):
    updated_product_url = await crud.update_product_url(db=db, pu_id=pu_id, data=data)
    if not updated_product_url:
        return error_response(
            message="Product URL not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(
        message="Product URL updated successfully.",
        data=updated_product_url
    )
    
@router.delete(
    "/{pu_id}",
    response_model=ResponseModel[None],
    dependencies=[Depends(get_current_user)]
)
async def delete_product_url(pu_id: str, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_product_url(db=db, pu_id=pu_id)
    if not deleted:
        return error_response(
            message="Product URL not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(
        message="Product URL deleted successfully.",
        data=None
    )