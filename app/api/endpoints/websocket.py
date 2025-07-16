import json
import os

from fastapi import APIRouter, WebSocket, Depends, Path, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db, AsyncSessionLocal
from app.crud import crud_price, crud_user, crud_stock
from app.schemas.news import News
from app.schemas.price import PriceUpdate, PriceBase, VolumeBase
from app.schemas.user import User
import asyncio
import random
import time
import uuid
from openai import OpenAI
from typing import Dict


class DataClient:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.is_bound = False

    def send_json(self, data: Dict):
        return self.websocket.send_json(data)

    def bind(self):
        self.is_bound = True

    def accept(self):
        return self.websocket.accept()

    def close(self):
        return self.websocket.close()

    def receive_text(self):
        return self.websocket.receive_text()


router = APIRouter()
data_clients = set()
news_clients = set()
last_news = None
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
active_users: Dict[str, WebSocket] = {}  # 이메일: WebSocket 매핑

# 심볼별 시장 상태 저장
symbol_states: Dict[str, Dict[str, float]] = {}


async def price_generator():
    print("📈 Price generator started")
    symbols = []
    last_price: Dict[str, float] = {}

    async with AsyncSessionLocal() as db:
        stocks = await crud_stock.get_stock_list(db)
        symbols = [stock.symbol for stock in stocks]
        for symbol in symbols:
            history = await crud_price.get_recent_price_history(db, symbol=symbol)
            last_price[symbol] = history[-1].close if history else 69000
            # 초기 상태 설정
            symbol_states[symbol] = {
                "trend": random.choice([-1, 1]),
                "volatility": random.uniform(0.5, 2.0),
            }

    while True:
        await asyncio.sleep(1)
        price_update_dict: Dict[str, Dict] = {}
        close_price_dict: Dict[str, float] = {}

        for symbol in symbols:
            t = int(time.time())
            state = symbol_states[symbol]
            base_price = last_price[symbol]

            # 상태 기반 변화량 계산
            trend = state["trend"]
            volatility = state["volatility"]
            sigma = base_price * volatility / 100
            delta = random.gauss(mu=trend * sigma * 0.1, sigma=sigma * 0.5)

            # 캔들 생성
            open_price = base_price
            close_price = max(1000, int(open_price + delta))
            high_price = max(open_price, close_price) + random.randint(0, 10)
            low_price = min(open_price, close_price) - random.randint(0, 10)

            # 가격 업데이트 객체
            price_update = PriceUpdate(
                candle=PriceBase(time=t, open=open_price, high=high_price, low=low_price, close=close_price),
                volume=VolumeBase(
                    time=t,
                    value=random.randint(100, 500),
                    color="#26a69a" if close_price >= open_price else "#ef5350"
                ),
                initial=False,
                symbol=symbol
            )

            price_update_dict[symbol] = price_update.model_dump()
            close_price_dict[symbol] = close_price

            # DB 저장
            async with AsyncSessionLocal() as db:
                await crud_price.create_price_record(db, price_update)

            # 상태 갱신
            if random.random() < 0.05:
                state["trend"] *= -1
            if random.random() < 0.1:
                state["volatility"] = random.uniform(0.5, 2.0)

        # 클라이언트 전송
        dead_clients = set()
        for client in data_clients:
            try:
                if not client.is_bound:
                    continue
                await client.send_json(price_update_dict)
            except Exception as e:
                print("Price WebSocket 연결 오류, 클라이언트 제거:", e)
                dead_clients.add(client)
        data_clients.difference_update(dead_clients)
        last_price = close_price_dict


async def news_generator():
    global latest_news
    headlines = [
        "신제품 출시로 매출 기대감 ↑",
        "CEO 교체 발표, 경영 전략 변화 예고",
        "글로벌 공급망 개선, 수익성 회복 조짐",
        "시장 점유율 하락 우려",
        "경기 침체 우려로 투자심리 위축",
    ]

    while True:
        print("📰 News generating...")
        await asyncio.sleep(random.randint(20, 40))

        prompt = random.choice(headlines)

        model = "gpt-4"
        messages = [
            {"role": "system",
             "content":
             "주식 시장 관련 헤드라인을 1개 작성해줘. 헤드라인은 20자 이내고 주목을 끌어야 "
             "하며, 긍정적 또는 부정적인 영향을 줄 수 있어야 해. 내용은 실제 주식 종목이나 "
             "실제 기업, 실제 인물 실명을 언급하지 말고 만들어줘"},
            {"role": "user", "content": prompt},
        ]
        response_format = {"type": "text"}

        try:
            response = openai_client.chat.completions.create(
                model=model,
                response_format=response_format,
                messages=messages
            )
            if response and response.choices and response.choices[0].message.content:
                headline = response.choices[0].message.content.strip()
            else:
                headline = "기본 헤드라인입니다."
        except Exception as e:
            print("OpenAI 오류:", e)
            headline = prompt

        sentiment = round(random.uniform(-1, 1), 2)
        impact = random.randint(1, 10)

        news = News(
            id=str(uuid.uuid4()),
            headline=headline,
            sentiment=sentiment,
            impact=impact,
            timestamp=int(time.time())
        )
        latest_news = news

        dead = set()
        for client in news_clients:
            try:
                await client.send_json(news.dict())
            except:
                dead.add(client)
        news_clients.difference_update(dead)
        print("📢 뉴스 전송됨:", news.headline)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    client = DataClient(websocket)
    await client.accept()
    data_clients.add(client)
    try:
        symbols = []
        async with AsyncSessionLocal() as db:
            stocks = await crud_stock.get_stock_list(db)
            symbols = [stock.symbol for stock in stocks]

        response = {}
        for symbol in symbols:
            response[symbol] = []
            async with AsyncSessionLocal() as db_session_for_history:
                history = await crud_price.get_recent_price_history(
                    db_session_for_history, seconds=1200, symbol=symbol)
            for record in history:
                price_update = PriceUpdate(
                    candle=PriceBase(time=record.time, open=record.open,
                                     high=record.high, low=record.low, close=record.close),
                    volume=VolumeBase(time=record.time,
                                      value=record.volume, color=record.color),
                    initial=True,
                    symbol=symbol
                )
                response[symbol].append(price_update.model_dump())
        await asyncio.sleep(0)
        await client.send_json(response)
        client.bind()
        while True:
            await client.receive_text()
    except Exception as e:
        print("Init history WebSocket 연결 오류:", e)
        await client.close()
        data_clients.discard(client)


@router.websocket("/ws/news")
async def websocket_news(websocket: WebSocket):
    await websocket.accept()
    news_clients.add(websocket)
    try:
        if latest_news:
            await websocket.send_json(latest_news.dict())
        while True:
            await websocket.receive_text()
    except:
        news_clients.remove(websocket)


@router.websocket("/ws/user/{email}")
async def websocket_user(websocket: WebSocket, email: str = Path(...), db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    active_users[email] = websocket
    print(f"🔌 User WebSocket 연결됨: {email}")

    try:
        while True:
            model_user = await crud_user.get_user_by_email(db, email)
            cur_user = User(
                id=model_user.id,
                username=model_user.username,
                email=model_user.email,
                full_name=model_user.full_name,
                balance=model_user.balance,
                invested_money=model_user.invested_money,
                stocks=model_user.stocks,
                portfolio=model_user.portfolio
            )
            await websocket.send_json(cur_user.model_dump())
            await asyncio.sleep(30)
    except WebSocketDisconnect:
        print(f"❌ User WebSocket 연결 해제됨: {email}")
        active_users.pop(email)
