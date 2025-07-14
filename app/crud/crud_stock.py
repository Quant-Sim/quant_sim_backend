from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import models
import time
async def get_stock_list(db: AsyncSession):
    query = select(models.Stocks)
    result = await db.execute(query)
    return result.scalars().all()