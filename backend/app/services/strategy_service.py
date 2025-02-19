from app.services.bithumb_api_client import get_orderbook, get_balance
from app.models.trading_model import OrderbookResponse, BalanceResponse
from typing import Tuple
from app.exceptions.custom_exceptions import BusinessLogicError
from app.config.config import settings
from app.utils.logger import logger

'''

거래 전략 수립 및 주문 정보 생성

Trading View에서 제공하는 거래 전략을 기반으로 매수/매도 주문 정보를 생성합니다.

'''

def get_current_strategy():
    """
    현재 설정된 전략 정보를 반환하는 함수
    """
    return {
        "strategy": "USDT Premium Strategy",
        "buy_percent": settings.BUY_PERCENT,
        "sell_percent": settings.SELL_PERCENT
    }



def usdt_premium_strategy(signal: str) -> Tuple[bool, str, str, float, float]:
    """
    USDT 프리미엄 전략 실행
    - 실행 여부(should_execute), 매수/매도 시그널, 코인, 수량, 가격을 반환
    """
    
    symbol = "USDT"

    if signal not in {"buy", "sell"}:
        raise BusinessLogicError("잘못된 거래 신호")

    balance: BalanceResponse = get_balance(symbol)
    total_usdt = balance.total_currency  

    if total_usdt is None:
        raise BusinessLogicError("USDT 잔고 정보를 가져올 수 없습니다.")
    
    long_position = total_usdt > 0


    strategy_result = dict()

    strategy_result["strategy"] = "usdt_premium"
    strategy_result["result"] = "Execute trade"


    #for test
    #make_buy_order_info(symbol, settings.BUY_PERCENT)


    if signal == "buy" and not long_position:
        logger.info(f"전략 평가 결과: {strategy_result}")
        units, price = make_buy_order_info(symbol, settings.BUY_PERCENT)
        return True, "buy", symbol, units, price  

    elif signal == "sell" and long_position:
        logger.info(f"전략 평가 결과: {strategy_result}")
        units, price = make_sell_order_info(symbol, settings.SELL_PERCENT)
        return True, "sell", symbol, units, price
    else:
        strategy_result["result"] = "Skip"
        logger.info(f"전략 평가 결과: {strategy_result}")
        return False, signal, "", 0, 0  # 실행 불가능 (should_execute=False)
    


def make_buy_order_info(order_currency: str, percent: float = 0.1) -> Tuple[float, float]:
    """
    매수 수량 계산 : 지정된 비율만큼 매수 주문 수량 계산

    Args:
        order_currency (str): 매수할 코인 (예: USDT)
        percent (float): 투자 비율 (0~1), 기본 10%

    Returns:
        tuple: (매수 수량, 예상 가격)
    """
    # 매수 호가 조회
    orderbook: OrderbookResponse = get_orderbook(order_currency)

    if not orderbook.asks:
        raise BusinessLogicError(f"{order_currency}의 매도 주문이 존재하지 않습니다.")

    lowest_ask_price = orderbook.asks[0].price  # 최저 매도 가격

    # 보유 KRW 조회
    balance: BalanceResponse = get_balance(order_currency)

    if balance.total_krw is None or balance.total_krw <= 0:
        raise BusinessLogicError("매수할 원화 잔액이 부족합니다.")

    # 매수 금액 계산 (비율 적용)
    final_krw = int(balance.total_krw * percent)

    # 매수 수량 계산
    unit = round(final_krw / lowest_ask_price, 8)

    if unit <= 0:
        raise BusinessLogicError("매수할 수량이 0 이하입니다.")
    

    buy_order_info = dict()
    buy_order_info["order_currency"] = order_currency
    buy_order_info["total_krw"] = str(round(balance.total_krw))
    buy_order_info["percent"] = f"{percent*100}%"
    buy_order_info["final_krw"] = str(final_krw)
    buy_order_info["units"] = str(unit)
    buy_order_info["price"] = str(lowest_ask_price)

    logger.info(f"주문 요청 정보: {buy_order_info}")

    return unit, lowest_ask_price


def make_sell_order_info(order_currency: str, percent: float = 1) -> Tuple[float, float]:
    """
    매도 수량 계산 : 지정된 비율만큼 매도 주문 수량 계산

    Args:
        order_currency (str): 매도할 코인 (예: USDT)
        percent (float): 매도 비율 (0~1), 기본 100%

    Returns:
        tuple: (매도 수량, 예상 가격)
    """

    # 매도 호가 조회
    orderbook: OrderbookResponse = get_orderbook(order_currency)
    
    if not orderbook.bids:
        raise BusinessLogicError(f"{order_currency}의 매도 호가 정보가 없습니다.")

    highest_bid_price = orderbook.bids[0].price  # 가장 높은 매수 호가

    # 보유 코인 수량 조회
    balance: BalanceResponse = get_balance(order_currency)

    if balance.available_currency is None or balance.available_currency <= 0:
        raise BusinessLogicError(f"{order_currency}의 매도 가능 잔액이 부족합니다.")

    # 매도 수량 계산 (비율 적용)
    final_coin = balance.available_currency * percent
    unit = round(final_coin, 8)

    if unit <= 0:
        raise BusinessLogicError("매도할 수량이 0 이하입니다.")

    return unit, highest_bid_price


def calculate_order_amount(balance_krw: float, target_price: float, percent: float) -> float:
    """
    추가 전략: 주어진 잔액과 목표 가격에 따라 주문 수량 계산
    """
    if balance_krw <= 0:
        raise BusinessLogicError("잔액이 부족하여 주문할 수 없습니다.")
    if target_price <= 0:
        raise BusinessLogicError("유효하지 않은 목표 가격입니다.")
    
    invest_krw = balance_krw * percent
    return round(invest_krw / target_price, 8)

def calculate_profit(entry_price: float, exit_price: float, quantity: float) -> float:
    """
    수익 계산 전략: 매수/매도 가격과 수량으로 수익 계산
    """
    if quantity <= 0:
        raise BusinessLogicError("거래 수량이 0 이하입니다.")
    if entry_price <= 0 or exit_price <= 0:
        raise BusinessLogicError("유효하지 않은 가격 값입니다.")
    
    return round((exit_price - entry_price) * quantity, 2)
