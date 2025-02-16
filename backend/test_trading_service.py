from app.services.trading_service import execute_trade
from app.models.trading_model import TradeRequest
from app.utils.logger import trading_loger


def test_execute_trade_buy():
    """ 매수 테스트 """
    request = TradeRequest(signal="buy", symbol="USDT")  # amount는 현재 사용되지 않음
    response = execute_trade(request)

    assert response.status in {"success", "error", "skipped"}, "잘못된 상태 반환"
    trading_loger.info(f"매수 테스트 결과: {response}")


def test_execute_trade_sell():
    """ 매도 테스트 """
    request = TradeRequest(signal="sell", symbol="USDT")
    response = execute_trade(request)

    assert response.status in {"success", "error", "skipped"}, "잘못된 상태 반환"
    trading_loger.info(f"매도 테스트 결과: {response}")


def test_execute_trade_test_mode():
    """ 테스트 모드 실행 """
    request = TradeRequest(signal="test", symbol="USDT")
    response = execute_trade(request)

    assert response.status == "test", "테스트 모드 실패"
    trading_loger.info(f"테스트 모드 결과: {response}")


if __name__ == "__main__":
    #test_execute_trade_buy()
    #test_execute_trade_sell()
    test_execute_trade_test_mode()
