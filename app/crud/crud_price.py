from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import models
from app.schemas.price import PriceUpdate
import time

async def create_price_record(db: AsyncSession, price_update: PriceUpdate):
    db_price = models.PriceHistory(
        symbol=price_update.symbol,
        time=price_update.candle.time,
        open=price_update.candle.open,
        high=price_update.candle.high,
        low=price_update.candle.low,
        close=price_update.candle.close,
        volume=price_update.volume.value,
        color=price_update.volume.color
    )
    db.add(db_price)
    await db.commit()
    await db.refresh(db_price)
    return db_price

async def get_recent_price_history(db: AsyncSession, seconds: int = 1200):
    start_time = int(time.time()) - seconds
    query = select(models.PriceHistory).filter(models.PriceHistory.time >= start_time).order_by(models.PriceHistory.time)
    result = await db.execute(query)
    return result.scalars().all()