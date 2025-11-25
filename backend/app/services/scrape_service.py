from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Product, ProductURL, PriceHistory
from app.services.scraper import fetch_page, extract_price
from uuid import UUID
from typing import List

async def scrape_product(db: AsyncSession, product: Product) -> List[float] | None:
    """Scrape the product's price from its URL and return the price."""
    
    returned_prices = []
    
    # Fetch the product URLs
    results = await db.execute(
        ProductURL.select().where(ProductURL.c.product_id == product.id)
    )
    product_url_records = await results.scalars().all()
    
    for record in product_url_records:
        url = record.url
        
        html_content = await fetch_page(url)
        if not html_content:
            continue
        
        price = extract_price(html_content)
        if price is None:
            continue
        
        # upate product current price and last checked
        product.current_price = price
        product.last_checked = func.now()
        
        # create a new price history record
        new_price_history = PriceHistory(
            product_id=product.id,
            product_url_id=record.id,
            price=price
        )
        db.add(new_price_history)
        await db.commit()
        await db.refresh(product)
        returned_prices.append(price)
        
    if returned_prices:
        return returned_prices
    return None

async def scrape_all_products(db: AsyncSession) -> List[dict] | None:
    """Scrape prices for all products in the database."""
    
    results = await db.execute(Product.select())
    products = await results.scalars().all()
    returned_data = []
    
    for product in products:
        prices = await scrape_product(db, product)
        if prices:
            returned_data.append({
                "product_id": product.id,
                "name": product.name,
                "scraped_prices": prices
            })
     
    if returned_data:   
        return returned_data
    return None
    