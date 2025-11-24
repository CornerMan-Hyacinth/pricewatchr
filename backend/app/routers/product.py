from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import crud
from app.database import get_db
from app.schemas import ProductInDB, ProductCreate, ProductUpdate, ResponseModel
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ResponseModel[ProductInDB], status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate, db: AsyncSession = Depends(get_db)):
    user_products = await crud.get_products_by_user(db=db, user_id=data.user_id)
    for product in user_products:
        if product.name == data.name:
            return error_response(
                status=status.HTTP_400_BAD_REQUEST,
                message="Product with this name already exists for the user.",
            )
            
    new_product = await crud.create_product(db=db, data=data)
    return success_response(
        status=status.HTTP_201_CREATED,
        message="Product created successfully.",
        data=new_product
    )
    
@router.get("/{product_id}", response_model=ResponseModel[ProductInDB])
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    product = await crud.get_product_by_id(db=db, product_id=product_id)
    if not product:
        return error_response(
            status=status.HTTP_404_NOT_FOUND,
            message="Product not found."
        )
        
    return success_response(
        status=status.HTTP_200_OK,
        message="Product retrieved successfully.",
        data=product
    )
    
@router.get("/user/{user_id}", response_model=ResponseModel[List[ProductInDB]])
async def get_products_by_user(user_id: str, db: AsyncSession = Depends(get_db)):
    products = await crud.get_products_by_user(db=db, user_id=user_id)
    return success_response(
        status=status.HTTP_200_OK,
        message="Products retrieved successfully.",
        data=products
    )
    
@router.put("/{product_id}", response_model=ResponseModel[ProductInDB])
async def update_product(product_id: str, data: ProductUpdate, db: AsyncSession = Depends(get_db)):
    product = await crud.get_product_by_id(db=db, product_id=product_id)
    if not product:
        return error_response(
            status=status.HTTP_404_NOT_FOUND,
            message="Product not found."
        )
        
    updated_product = await crud.update_product(db=db, product_id=product_id, data=data)
    return success_response(
        status=status.HTTP_200_OK,
        message="Product updated successfully.",
        data=updated_product
    )
    
@router.delete("/{product_id}", response_model=ResponseModel[None])
async def delete_product(product_id: str, db: AsyncSession = Depends(get_db)):
    product = await crud.get_product_by_id(db=db, product_id=product_id)
    if not product:
        return error_response(
            status=status.HTTP_404_NOT_FOUND,
            message="Product not found."
        )
        
    await crud.delete_product(db=db, product_id=product_id)
    return success_response(
        status=status.HTTP_200_OK,
        message="Product deleted successfully.",
        data=None
    )