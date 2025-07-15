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
        models.Stocks(symbol="DOGE", name="도찌코인", sector="Coin", industry="Cryptocurrency"),
        models.Stocks(symbol="MAN", name="맹구", sector="Technology", industry="Internet Services"),
        models.Stocks(symbol="BTC", name="비트컴퍼니", sector="Coin", industry="Cryptocurrency"),
        models.Stocks(symbol="AMANG", name="아망존", sector="Technology", industry="E-Commerce"),
        models.Stocks(symbol="NETF", name="넷뿌릭스", sector="Media", industry="Streaming"),
        models.Stocks(symbol="BANG", name="방타", sector="Entertainment", industry="Music & Talent"),
        models.Stocks(symbol="NVDH", name="느비디야", sector="Semiconductors", industry="AI Chips"),
        models.Stocks(symbol="INTA", name="인텔레기야", sector="Semiconductors", industry="Processors"),
        models.Stocks(symbol="KAKO", name="카카웃", sector="Technology", industry="Platform Services"),
        models.Stocks(symbol="DAUM", name="다우미", sector="Technology", industry="Search Engines"),
        models.Stocks(symbol="APPL", name="사과전자", sector="Technology", industry="Consumer Electronics"),
        models.Stocks(symbol="MSFT", name="윈도소프트", sector="Technology", industry="Software"),
        models.Stocks(symbol="TSLY", name="테슬라리", sector="Automotive", industry="Electric Vehicles"),
        models.Stocks(symbol="YUTB", name="윳튜브", sector="Media", industry="Streaming"),
        models.Stocks(symbol="TWIT", name="트윗컴퍼니", sector="Media", industry="Social Media"),
        models.Stocks(symbol="CHTGP", name="챗지피", sector="AI", industry="LLM Services"),
        models.Stocks(symbol="XION", name="쑈핑온", sector="E-Commerce", industry="Online Retail"),
        models.Stocks(symbol="KONI", name="코인이즈", sector="Finance", industry="Crypto Exchange"),
        models.Stocks(symbol="LAMB", name="램램컴퍼니", sector="Semiconductors", industry="Memory"),
        models.Stocks(symbol="SPCE", name="스페이슬", sector="Aerospace", industry="Space Tourism"),
        models.Stocks(symbol="BYND", name="비욘미트", sector="Food", industry="Plant-Based"),
        models.Stocks(symbol="MUNG", name="멍청이컴퍼니", sector="Finance", industry="Speculation"),
        models.Stocks(symbol="GPTX", name="지피텍", sector="AI", industry="Foundation Models"),
        models.Stocks(symbol="ZKDL", name="지케이딜라이트", sector="Blockchain", industry="ZKP Infra"),
        models.Stocks(symbol="VIRS", name="바이러스랩", sector="Healthcare", industry="Biotech"),
        models.Stocks(symbol="CURE", name="큐어컴퍼니", sector="Healthcare", industry="Pharmaceuticals"),
        models.Stocks(symbol="HYBE", name="하이브스타", sector="Entertainment", industry="Music Label"),
        models.Stocks(symbol="RIBL", name="리블네트웍스", sector="Blockchain", industry="Payments"),
        models.Stocks(symbol="STPD", name="스탑다오", sector="DAO", industry="Governance"),
        models.Stocks(symbol="MOON", name="문익점테크", sector="Energy", industry="Lunar Mining"),
        models.Stocks(symbol="LGND", name="레전드컴퍼니", sector="Gaming", industry="eSports"),
        models.Stocks(symbol="PLUG", name="플러그앤파워", sector="Energy", industry="Hydrogen Fuel"),
        models.Stocks(symbol="MEGA", name="메가테크", sector="Technology", industry="Quantum Computing"),
        models.Stocks(symbol="BAEK", name="백종원푸드", sector="Food", industry="F&B Franchise"),
        models.Stocks(symbol="BBQ", name="바비큐랩스", sector="Food", industry="Delivery Tech"),
        models.Stocks(symbol="GFX", name="지에프엑스", sector="Gaming", industry="Game Engines"),
        models.Stocks(symbol="PIX", name="픽셀테크", sector="AR/VR", industry="Immersive Tech"),
        models.Stocks(symbol="TUBE", name="튜브에어", sector="Media", industry="UGC Video"),
        models.Stocks(symbol="BIRD", name="새컴퍼니", sector="Aerospace", industry="Drone Delivery"),
        models.Stocks(symbol="ICEC", name="아이스크림에듀", sector="Education", industry="EdTech"),
        models.Stocks(symbol="NONG", name="농심이즈", sector="Food", industry="Instant Food"),
        models.Stocks(symbol="COKE", name="콬컴퍼니", sector="Beverage", industry="Drinks"),
        models.Stocks(symbol="MBTI", name="엠비티아이랩", sector="Psychology", industry="Personality AI"),
        models.Stocks(symbol="DANK", name="댕크스탁", sector="Meme", industry="Stonk Market"),
        models.Stocks(symbol="KIC", name="기억외장화", sector="AI", industry="Memory-as-a-Service")
    ]

    db.add_all(stock_entries)
    await db.commit()
