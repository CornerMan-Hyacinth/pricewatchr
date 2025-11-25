from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.crud import get_product_by_id
from app.database import get_db
from app.services.scrape_service import scrape_product, scrape_all_products
from app.utils.response import success_response, error_response
from app.schemas.response import ResponseModel, ScrapeAllResponse, ScrapeProductResponse

router = APIRouter(prefix="/scrape", tags=["Scraper"])

@router.post("/all", response_model=ResponseModel[ScrapeAllResponse])
async def scrape_all(db: AsyncSession = Depends(get_db)):
    """Scrape prices for all products."""
    scraped_data = await scrape_all_products(db)
    if scraped_data is None:
        return success_response(
            message="No products were scraped.",
            status_code=status.HTTP_204_NO_CONTENT
        )
        
    return success_response(
        message="All products scraped successfully.",
        data=ScrapeAllResponse(
            status="SUCCESS",
            count=len(scraped_data),
            results=scraped_data
        )
    )
    
@router.post("/{product_id}", response_model=ResponseModel[ScrapeProductResponse])
async def scrape_product(product_id: UUID, db: AsyncSession = Depends(get_db)):
    """Scrape price for a specific product by its ID."""
    
    product = await get_product_by_id(db, product_id)
    
    if not product:
        return error_response(
            message="Product not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )
        
    scraped_prices = await scrape_product(db, product)
    if scraped_prices is None:
        return success_response(
            message="No prices were scraped for the product.",
            status_code=status.HTTP_204_NO_CONTENT
        )
        
    return success_response(
        message="Product scraped successfully.",
        data=ScrapeProductResponse(
            status="SUCCESS",
            product_id=product.id,
            name=product.name,
            scraped_prices=scraped_prices
        )
    )