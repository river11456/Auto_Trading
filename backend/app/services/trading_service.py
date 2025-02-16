from app.services.bithumb_api_client import (
    order_market_buy, order_market_sell, get_user_transactions
)
from app.services.strategy_service import usdt_premium_strategy
from app.models.trading_model import TradeRequest, TradeResponse
from app.utils.logger import logger
import random
from typing import Tuple

def execute_trade(request: TradeRequest) -> TradeResponse:

    """
    웹훅 알러트 기반 거래 실행 함수
    """
    # TEST 모드 여부 확인
    if request.signal == "test":
        return generate_test_trade_response()


    # 전략 실행
    should_execute, signal, symbol, units, price = usdt_premium_strategy(request.signal)
  

    if not should_execute:
        logger.info("전략 조건 미충족으로 거래 미실시")
        return generate_skipped_trade_response()

    if signal == "buy":
        logger.info("usdt_premium 전략에 따라 매수 진행")
        result = order_market_buy(units, symbol)
        message = "매수 성공" if result.get("status") == "0000" else "매수 실패"
    
    elif signal == "sell":
        logger.info("usdt_premium 전략에 따라 매도 진행")
        result = order_market_sell(units, symbol)
        message = "매도 성공" if result.get("status") == "0000" else "매도 실패"
    
    else:
        raise ValueError("잘못된 거래 신호")
    

    # 거래 성공 시 거래 내역 가져오기
    if result.get("status") == "0000":
        units, price, fee, net_settlement = fetch_latest_transaction(symbol, signal)
    else:
        units, price, fee, net_settlement = 0, 0, 0, 0


    return TradeResponse(
        status="success" if result.get("status") == "0000" else "error",
        message=message,
        order_id=result.get("order_id", ""),
        filled_quantity=units,
        avg_price=price,
        fee=fee,
        net_settlement=net_settlement
    )







def generate_skipped_trade_response() -> TradeResponse:
    """
    전략 조건 미충족 시 거래 실행 안함 응답 반환
    """
    return TradeResponse(
        status="skipped",
        message="전략 조건 미충족",
        order_id="",
        filled_quantity=0,
        avg_price=0,
        fee=0,
        net_settlement=0
    )

def generate_test_trade_response() -> TradeResponse:
    """
    "test" 모드: 가상의 거래 데이터를 생성하여 반환
    """
    symbol = "TEST"
    units = 9999
    price = 9999
    fee = 9999
    net_settlement = 9999

    return TradeResponse(
        status="test",
        message="가상 거래 테스트 실행됨",
        order_id="TEST_ORDER_ID",
        filled_quantity=units,
        avg_price=price,
        fee=fee,
        net_settlement=net_settlement
    )


def fetch_latest_transaction(symbol: str, signal: str) -> Tuple[float, float, float, float]:
    """
    최근 거래 내역을 가져와 거래 수량, 평균 가격, 수수료 및 최종 정산 금액을 반환하는 함수.

    Args:
        symbol (str): 거래한 자산 (예: USDT)
        signal (str): 거래 신호 (buy 또는 sell)

    Returns:
        Tuple[float, float, float, float]: (거래 수량, 평균 가격, 수수료, 최종 정산 금액)
    """
    try:
        transactions = get_user_transactions(order_currency=symbol, payment_currency="KRW", count=1)
        latest_transaction = transactions.transactions[0] if transactions.transactions else None

        if latest_transaction:
            units = latest_transaction.units  # 체결된 수량
            price = latest_transaction.price  # 체결 가격
            fee = latest_transaction.fee  # 거래 수수료
            net_settlement = latest_transaction.amount - fee if signal == "sell" else -(latest_transaction.amount + fee)
            net_settlement = round(net_settlement)
        else:
            units, price, fee, net_settlement = 0, 0, 0, 0

    except Exception as e:
        units, price, fee, net_settlement = 0, 0, 0, 0
        logger.error(f"거래 내역 조회 실패: {e}")

    return units, price, fee, net_settlement
