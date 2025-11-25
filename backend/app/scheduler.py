from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database import SessionLocal
from app.services.scrape_service import scrape_all_products

scheduler = AsyncIOScheduler()

async def scrape_job():
    async with SessionLocal() as db:
        await scrape_all_products(db)
        
def init_scheduler():
    scheduler.add_job(
        scrape_job,
        'interval',
        hours=1,
        id='scrape_job',
        replace_existing=True,
        coalesce=True,
        max_instances=1
    )
    scheduler.start()
    
async def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()