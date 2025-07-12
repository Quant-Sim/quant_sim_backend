from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db import models
from app.schemas import order as order_schema

def create_order(db: Session, order: order_schema.OrderCreate, user_id: int):
    """
    매수/매도 주문을 생성하고 사용자의 자산과 포트폴리오를 업데이트합니다.
    이 함수는 하나의 트랜잭션으로 처리되어야 합니다.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    stock = db.query(models.Stock).filter(models.Stock.id == order.stock_id).first()

    if not user or not stock:
        raise HTTPException(status_code=404, detail="사용자 또는 주식을 찾을 수 없습니다.")

    total_cost = order.price * order.quantity

    if order.order_type == models.OrderType.BUY:
        # --- 매수 로직 ---
        if user.cash_balance < total_cost:
            raise HTTPException(status_code=400, detail="현금이 부족합니다.")

        user.cash_balance -= total_cost

        portfolio_item = db.query(models.Portfolio).filter_by(user_id=user.id, stock_id=stock.id).first()
        if portfolio_item:
            # 기존 보유 종목
            new_quantity = portfolio_item.quantity + order.quantity
            new_avg_price = ((portfolio_item.average_buy_price * portfolio_item.quantity) + total_cost) / new_quantity
            portfolio_item.quantity = new_quantity
            portfolio_item.average_buy_price = new_avg_price
        else:
            # 신규 매수 종목
            portfolio_item = models.Portfolio(
                user_id=user.id,
                stock_id=stock.id,
                quantity=order.quantity,
                average_buy_price=order.price
            )
            db.add(portfolio_item)

    elif order.order_type == models.OrderType.SELL:
        # --- 매도 로직 ---
        portfolio_item = db.query(models.Portfolio).filter_by(user_id=user.id, stock_id=stock.id).first()
        if not portfolio_item or portfolio_item.quantity < order.quantity:
            raise HTTPException(status_code=400, detail="보유 주식이 부족합니다.")

        user.cash_balance += total_cost
        portfolio_item.quantity -= order.quantity

        # 보유 수량이 0이 되면 포트폴리오에서 삭제할 수도 있습니다.
        if portfolio_item.quantity == 0:
            db.delete(portfolio_item)

    # 주문 기록 생성
    db_order = models.Order(**order.model_dump(), user_id=user.id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order