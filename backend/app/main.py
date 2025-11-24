from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.database import Base, engine
from app.schemas import ResponseModel, ResponseStatus
from app.routers import product, productUrl, priceHistory

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    
    await engine.dispose()
    
app = FastAPI(
    title="PriceWatchr API",
    description="API for PriceWatchr application to monitor product prices.",
    summary="PriceWatchr API",
    version="0.1.0",
    lifespan=lifespan
)

@app.include_router(product.router)
@app.include_router(productUrl.router)
@app.include_router(priceHistory.router)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ResponseModel(
            status=ResponseStatus.ERROR,
            message=str(exc),
            data=None
        ).model_dump()
    )