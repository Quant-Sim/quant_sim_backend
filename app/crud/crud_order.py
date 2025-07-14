from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import models
from app.schemas.order import OrderCreate
import time
import random
from fastapi import HTTPException

async def create_order(db: AsyncSession, order: OrderCreate):
    timestamp_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    total_val = round(order.price * order.quantity)

    result = await db.execute(select(models.User).where(models.User.id == order.user_id))
    user = result.scalar_one_or_none()
    await db.refresh(user)  # 👈 여기에 넣으면 됩니다

    if order.type == '매수':
        if user.balance < total_val:
            raise HTTPException(status_code=400, detail="잔액이 부족합니다.")
        user.balance -= total_val
        user.invested_money += total_val
        exists = False
        for stock in user.stocks:
            if stock["symbol"] == order.symbol:
                stock["total"] = total_val + stock["quantity"] * order.price
                stock["quantity"] += order.quantity
                stock["price"] = round((stock["total"] / stock["quantity"]), 2)
                exists = True
                break
        if not exists:
            user.stocks.append({
                "name": order.name,
                "symbol": order.symbol,
                "price": order.price,
                "quantity": order.quantity,
                "total": total_val,
                "color": "green",
                "chartColor": "#" + ''.join(random.choices('0123456789abcdef', k=6)),
                "points": "0,0"
            })
    elif order.type == '매도':
        stock_found = False
        for stock in user.stocks:
            if stock["symbol"] == order.symbol:
                if stock["quantity"] < order.quantity:
                    raise HTTPException(status_code=400, detail="보유 주식 수가 부족합니다.")
                stock["quantity"] -= order.quantity
                stock["total"] = stock["quantity"] * order.price
                user.balance += total_val
                if stock["quantity"] == 0:
                    user.stocks.remove(stock)
                stock_found = True
                break
        if not stock_found:
            raise HTTPException(status_code=400, detail="해당 주식을 보유하고 있지 않습니다.")

    db_order = models.OrderHistory(
        user_id=order.user_id,
        symbol=order.symbol,
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

async def get_orders(db: AsyncSession, limit: int = 100, symbol: str = None):
    query = select(models.OrderHistory).filter(models.OrderHistory.symbol == symbol).order_by(models.OrderHistory.id.desc()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_user_orders(db: AsyncSession, symbol: str, user_id: int):
    query = select(models.OrderHistory).filter(
        models.OrderHistory.symbol == symbol,
        models.OrderHistory.user_id == user_id
    ).order_by(models.OrderHistory.id.desc())
    result = await db.execute(query)
    return result.scalars().all()