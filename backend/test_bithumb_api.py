from app.services.bithumb_api_client import (
    get_ticker,
    get_orderbook,
    get_balance,
    get_user_transactions,
    order_market_buy,
    order_market_sell
)


from app.utils.display import print_transaction_history, print_balance_info

def test_get_ticker():
    """ 티커 정보 조회 """
    response = get_ticker("BTC", "KRW")
    print(f"[Ticker] BTC 현재가: {response.closing_price} KRW")

def test_get_orderbook():
    """ 매수/매도 호가 조회 """
    response = get_orderbook("BTC", "KRW")
    #print(response)
    print(f"[Orderbook] BTC 최우선 매수호가: {response.bids[0].price} KRW")

def test_get_balance():
    """ 잔고 조회 """
    response = get_balance("USDT")
    #print(f"[Balance] BTC 보유량: {response.total_currency} BTC")
    print_balance_info("USDT",response)

def test_get_user_transactions():
    """ 거래 내역 조회 """
    response = get_user_transactions("USDT", "KRW", searchGb = 0)
    print(f"[Transactions] 최근 거래 개수: {len(response.transactions)}")
    print(f"[Transactions] 거래 내역 :\n")
    print_transaction_history(response)
    

def test_order_market_buy():
    """ 시장가 매수 (주의!) """
    response = order_market_buy(4, "USDT", "KRW")  # 소량 매수 테스트
    print(f"[Buy Order] 주문 완료 - 주문 ID: {response.get('order_id')}")

def test_order_market_sell():
    """ 시장가 매도 (주의!) """
    response = order_market_sell(4, "USDT", "KRW")  # 소량 매도 테스트
    print(f"[Sell Order] 주문 완료 - 주문 ID: {response.get('order_id')}")

if __name__ == "__main__":
    test_get_ticker()
    test_get_orderbook()
    test_get_balance()

    # ⚠️ 실제 매매 테스트를 원하면 주석 해제 후 실행
    #test_order_market_buy()
    #test_order_market_sell()

    #test_get_user_transactions()

