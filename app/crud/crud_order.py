from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import models
from app.schemas.order import OrderCreate
import time

async def create_order(db: AsyncSession, order: OrderCreate):
    timestamp_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    total_val = round(order.price * order.quantity)
    
    db_order = models.OrderHistory(
        timestamp=timestamp_str,
        time=int(time.time()),
        type=order.type,
        price=order.price,
        quantity=order.quantity,
        total=total_val
    )
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

async def get_orders(db: AsyncSession, limit: int = 100):
    query = select(models.OrderHistory).order_by(models.OrderHistory.id.desc()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()