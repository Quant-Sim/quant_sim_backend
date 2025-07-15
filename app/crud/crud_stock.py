from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import models
import time

async def get_stock_list(db: AsyncSession):
    query = select(models.Stocks)
    result = await db.execute(query)
    return result.scalars().all()

async def insert_initial_stocks(db: AsyncSession):
    stock_entries = [
        models.Stocks(symbol="HWG", name="황광호날두회사", sector="Technology", industry="Consumer Electronics"),
        models.Stocks(symbol="GOOGO", name="구골", sector="Technology", industry="Internet Services"),
        models.Stocks(symbol="TGLA", name="테킬라", sector="Automotive", industry="Electric Vehicles"),
        models.Stocks(symbol="BTC", name="비트컴퍼니", sector="Coin", industry="Cryptocurrency"),
    ]

    db.add_all(stock_entries)
    await db.commit()