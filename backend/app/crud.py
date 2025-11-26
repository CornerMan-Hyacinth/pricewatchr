from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import List, Optional
from app.models import User, Product, PriceHistory, ProductURL
from app.schemas.user import UserInDB
from app.schemas.productUrl import ProductUrlInDB, ProductUrlCreate, ProductUrlUpdate
from app.schemas.product import ProductInDB, ProductCreate, ProductUpdate
from app.schemas.priceHistory import PriceHistoryInDB, PriceHistoryCreate

#------ PRODUCT URL CRUD ------
async def create_product_url(db: AsyncSession, data: ProductUrlCreate) -> ProductUrlInDB:
    result = await db.execute(
        select(ProductURL)
        .where(ProductURL.product_id == data.product_id)
        .where(ProductURL.url == data.url.strip())
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        return ProductUrlInDB.model_validate(existing)
    
    new_product_url = ProductURL(**data.model_dump())
    db.add(new_product_url)
    await db.commit()
    await db.refresh(new_product_url)
    return ProductUrlInDB.model_validate(new_product_url)

async def get_product_urls_by_product(db: AsyncSession, product_id: UUID) -> List[ProductUrlInDB]:
    results = await db.execute(select(ProductURL).where(ProductURL.product_id == product_id))
    product_urls = results.scalars().all()
    return [ProductUrlInDB.model_validate(pu) for pu in product_urls]

async def get_product_url_by_id(db: AsyncSession, pu_id: UUID) -> Optional[ProductUrlInDB]:
    result = await db.execute(select(ProductURL).where(ProductURL.id == pu_id))
    product_url = result.scalars().first()
    if not product_url:
        return None
    
    return ProductUrlInDB.model_validate(product_url)

async def update_product_url(
    db: AsyncSession, pu_id: UUID, data: ProductUrlUpdate
) -> Optional[ProductUrlInDB]:
    result = await db.execute(select(ProductURL).where(ProductURL.id == pu_id))
    product_url = result.scalars().first()
    if not product_url:
        return None
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product_url, key, value)
        
    await db.commit()
    await db.refresh(product_url)
    return ProductUrlInDB.model_validate(product_url)

async def delete_product_url(db: AsyncSession, pu_id: UUID) -> bool:
    result = await db.execute(select(ProductURL).where(ProductURL.id == pu_id))
    product_url = result.scalars().first()
    if not product_url:
        return False
    
    await db.delete(product_url)
    await db.commit()
    return True
    

#------ PRODUCT CRUD ------
async def create_product(db: AsyncSession, data: ProductCreate, user_id: UUID) -> ProductInDB:
    product_dict = data.model_dump()
    product_dict["user_id"] = user_id
    
    new_product = Product(**product_dict)
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    
    # Create associated product URLs
    for i, url in enumerate(data.urls):
        await create_product_url(
            db=db,
            data=ProductUrlCreate(
                product_id=new_product.id,
                url=url,
                is_primary=(
                    url == data.urls[data.primary_url] if data.primary_url is not None else False
                ),
                retailer=data.retailers[i] if data.retailers and i < len(data.retailers) else None
            )
        )

    return ProductInDB.model_validate(new_product)

async def get_products_by_user(db: AsyncSession, user_id: UUID) -> List[ProductInDB]:
    results = await db.execute(select(Product).where(Product.user_id == user_id))
    user_products = results.scalars().all()
    return [ProductInDB.model_validate(p) for p in user_products]

async def get_product_by_id(db: AsyncSession, product_id: UUID) -> Optional[ProductInDB]:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        return None
    
    return ProductInDB.model_validate(product)

async def update_product(db: AsyncSession, product_id: UUID, data: ProductUpdate) -> Optional[ProductInDB]:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        return None
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
        
    await db.commit()
    await db.refresh(product)
    return ProductInDB.model_validate(product)

async def delete_product(db: AsyncSession, product_id: UUID) -> bool:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        return False
    
    await db.delete(product)
    await db.commit()
    return True

#------ PRICE HISTORY CRUD ------

async def create_price_history(db: AsyncSession, data: PriceHistoryCreate) -> PriceHistoryInDB:
    updated_product = await update_product(
        db=db, product_id=data.product_id, data=ProductUpdate(current_price=data.price)
    )
    if not updated_product:
        return None
    
    new_price_history = PriceHistory(**data.model_dump())
    db.add(new_price_history)
    await db.commit()
    await db.refresh(new_price_history)
    
    return PriceHistoryInDB.model_validate(new_price_history)

async def get_product_price_history(db: AsyncSession, product_id: UUID) -> List[PriceHistoryInDB]:
    results = await db.execute(select(PriceHistory).where(PriceHistory.product_id == product_id))
    price_histories = results.scalars().all()
    return [PriceHistoryInDB.model_validate(h) for h in price_histories]

async def get_price_history_by_id(db: AsyncSession, ph_id: UUID) -> Optional[PriceHistoryInDB]:
    result = await db.execute(select(PriceHistory).where(PriceHistory.id == ph_id))
    price_history = result.scalars().first()
    if not price_history:
        return None
    
    return PriceHistoryInDB.model_validate(price_history)

async def delete_price_history(db: AsyncSession, ph_id: UUID) -> bool:
    result = await db.execute(select(PriceHistory).where(PriceHistory.id == ph_id))
    price_history = result.scalars().first()
    if not price_history:
        return False
    
    await db.delete(price_history)
    await db.commit()
    return True