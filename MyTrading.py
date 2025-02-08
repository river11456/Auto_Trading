import requests
import os
import json
from xcoin_api import XCoinAPI


# 빗썸 API 키 설정 (환경변수로부터 읽어옴)
BITHUMB_API_KEY = os.getenv('BITHUMB_API_KEY')
BITHUMB_SECRET = os.getenv('BITHUMB_SECRET')
BITHUMB_API_URL = 'https://api.bithumb.com'

 # XCoinAPI 클래스 인스턴스 생성
client = XCoinAPI(BITHUMB_API_KEY, BITHUMB_SECRET)


def get_ticker(order_currency, payment_currency = "KRW"):
    '''
    마지막 체결정보(Tick)을 제공
    '''
    endpoint = '/public/ticker/{}_{}'.format(order_currency, payment_currency)

    headers = {"accept": "application/json"}

    response = requests.get(BITHUMB_API_URL+endpoint, headers=headers)

    result = response.json()

    #print(f"현재가 정보 조회:")
    #print(json.dumps(result, indent=4, ensure_ascii=False))

    return result

def get_orderbook(order_currency, payment_currency = "KRW"):
    '''
    매수/매도 호가 정보를 제공
    '''
    endpoint = '/public/orderbook/{}_{}'.format(order_currency, payment_currency)

    headers = {"accept": "application/json"}

    response = requests.get(BITHUMB_API_URL+endpoint, headers=headers, params={"count": 5})

    result = response.json()

    #print("API 응답:")
    #print(json.dumps(result, indent=4, ensure_ascii=False))

    return result




def get_account_info(order_currency,payment_currency = "KRW"):
    '''
    회원 정보 및 코인 별 거래 수수료 정보 제공
    '''
    endpoint = '/info/account'
    payload = {
        "order_currency": order_currency,
        "payment_currency": payment_currency
    }
    result = client.xcoinApiCall(endpoint,payload)

    #print("API 응답:")
    #print(json.dumps(result, indent=4, ensure_ascii=False))

    return result


def get_balance(currency):
    '''
    내 자산 정보 조회
    '''
    endpoint = '/info/balance'
    payload = {
        "currency": currency
    }
    result = client.xcoinApiCall(endpoint,payload)

    #print("API 응답:")
    #print(json.dumps(result, indent=4, ensure_ascii=False))

    return result


def order_market_buy(units, order_currency, payment_currency):
    '''
    시장가 매수 주문
    '''
    endpoint = '/trade/market_buy'
    payload = {
        "units": units,
        "order_currency": order_currency,
        "payment_currency": payment_currency      
    }

    result = client.xcoinApiCall(endpoint,payload)

    print("API 응답:")
    print(json.dumps(result, indent=4, ensure_ascii=False))

    return result

def order_market_sell(units, order_currency, payment_currency):
    '''
    시장가 매도 주문
    '''
    endpoint = '/trade/market_sell'
    payload = {
        "units": units,
        "order_currency": order_currency,
        "payment_currency": payment_currency      
    }

    result = client.xcoinApiCall(endpoint,payload)

    print("API 응답:")
    print(json.dumps(result, indent=4, ensure_ascii=False))

    return result



def get_market_price_units(order_currency, payment_currency = "KRW", percent = 0.1):
        
    orderbook = get_orderbook(order_currency)
    # 매도 호가 중 가장 낮은 가격 추출 (문자열을 실수로 변환)
    lowest_ask_price = float(orderbook["data"]["bids"][0]["price"])

    # 보유 중인 KRW 수량 조회
    balance = get_balance(order_currency)
    total_krw = int(float(balance["data"]["total_krw"]))
    #print(f"보유 중인 KRW: {total_krw} KRW")

    final_krw = int(total_krw * percent)
    print(f"매수할 KRW: {final_krw} KRW")

    # 구매 가능한 수량 계산
    result = round(final_krw / lowest_ask_price, 8)
    
    return result


if __name__ == "__main__":
 

    signal = "buy"
    

    if signal == "buy":

        # 구매 가능한 USDT 수량 계산
        USDT_quantity = get_market_price_units("USDT", percent=0.9)
        print(f"매수 가능한 USDT 수량: {USDT_quantity} USDT")

        # 시장가 전량 매수
        #order_market_buy(USDT_quantity, "USDT", "KRW")
        
    elif signal == "sell":

        # 보유 중인 USDT 수량 조회
        balance = get_balance("USDT")
        USDT_quantity = float(balance["data"]["total_usdt"])

        # 시장가 전량 매도
        order_market_sell(USDT_quantity, "USDT", "KRW")
    
    else:
        print("알 수 없는 신호입니다.")





