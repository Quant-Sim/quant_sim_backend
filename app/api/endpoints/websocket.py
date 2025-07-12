from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db, AsyncSessionLocal
from app.crud import crud_price
from app.schemas.price import PriceUpdate, PriceBase, VolumeBase
import asyncio
import random
import time

router = APIRouter()
clients = set()

async def price_generator():
    print("📈 Price generator started")
    async with AsyncSessionLocal() as db:
        history = await crud_price.get_recent_price_history(db)
        last_price = history[-1].close if history else 69000

    while True:
        await asyncio.sleep(1)
        t = int(time.time())
        delta = random.randint(-30, 30)
        open_price = last_price
        close_price = max(1000, open_price + delta)
        high_price = max(open_price, close_price) + random.randint(0, 10)
        low_price = min(open_price, close_price) - random.randint(0, 10)

        price_update = PriceUpdate(
            candle=PriceBase(time=t, open=open_price, high=high_price, low=low_price, close=close_price),
            volume=VolumeBase(time=t, value=random.randint(50, 150), color="#26a69a" if close_price >= open_price else "#ef5350")
        )
        
        async with AsyncSessionLocal() as db:
            await crud_price.create_price_record(db, price_update)

        dead_clients = set()
        for client in clients:
            try:
                await client.send_json(price_update.model_dump())
            except Exception:
                dead_clients.add(client)
        clients.difference_update(dead_clients)
        last_price = close_price

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    clients.add(websocket)
    try:
        history = await crud_price.get_recent_price_history(db, seconds=1200)
        for record in history:
            price_update = PriceUpdate(
                candle=PriceBase(time=record.time, open=record.open, high=record.high, low=record.low, close=record.close),
                volume=VolumeBase(time=record.time, value=record.volume, color=record.color),
                initial=True
            )
            await websocket.send_json(price_update.model_dump())
            await asyncio.sleep(0.001)

        while True:
            await websocket.receive_text()
    except Exception:
        clients.remove(websocket)