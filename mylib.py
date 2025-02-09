import requests
import os
import json
from xcoin_api import XCoinAPI
from rich.console import Console
from rich.table import Table


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

    try:
        result = client.xcoinApiCall(endpoint,payload)
        
        #print("API 응답:")
        #print(json.dumps(result, indent=4, ensure_ascii=False))

        return result
    
    except Exception as err:
        print(err)


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
    
    try:
        result = client.xcoinApiCall(endpoint,payload)

        #print("API 응답:")
        #print(json.dumps(result, indent=4, ensure_ascii=False))
        return result
    
    except Exception as err:
        print(err)

  

def make_order_info(signal, order_currency, payment_currency = "KRW", percent = 0.1):
        
    if signal == "buy":

        orderbook = get_orderbook(order_currency)
        # 매도 호가 중 가장 낮은 가격 추출 (문자열을 실수로 변환)
        lowest_ask_price = float(orderbook["data"]["asks"][0]["price"])

        # 보유 중인 KRW 수량 조회
        balance = get_balance(order_currency)
        total_krw = int(float(balance["data"]["total_krw"]))
        #print(f"보유 중인 KRW: {total_krw} KRW")

        final_krw = int(total_krw * percent)
        #print(f"매수할 KRW: {final_krw} KRW")

        # 구매 가능한 수량 계산
        unit = round(final_krw / lowest_ask_price, 8)

        price = lowest_ask_price

    elif signal == "sell":
        
        orderbook = get_orderbook(order_currency)
        # 매수 호가 중 가장 높은 가격 추출 (문자열을 실수로 변환)
        highest_bid_price = float(orderbook["data"]["bids"][0]["price"])

        # 보유 중인 코인 수량 조회
        balance = get_balance(order_currency)
        total_coin = float(balance["data"]["total_" + order_currency.lower()])
        #print(f"보유 중인 {order_currency}: {total_coin} {order_currency}")

        final_coin = total_coin * percent
        #print(f"매도할 {order_currency}: {final_coin} {order_currency}")

        # 구매 가능한 수량 계산
        unit = round(final_coin, 8)
  
        price = highest_bid_price

    return unit, price


console = Console()

def print_order_info(order_type, USDT_quantity, price, result):
    """
    주문 정보를 터미널에 출력하는 함수

    Parameters:
        order_type (str): "매수" 또는 "매도"
        USDT_quantity (float): 거래 수량 (USDT 단위)
        price (float): 체결 가격 (KRW)
        result (dict): API 응답 결과
    """

    # 🔴 매수 (red) / 🔵 매도 (blue) 색상 및 문구 결정
    order_color = "red" if order_type == "buy" else "blue"
    order_type = "매수" if order_type == "buy" else "매도"

    # 📌 주문 정보 테이블 생성
    table = Table(title="📌 주문 정보", show_header=True, header_style="bold magenta")
    table.add_column("항목", style="cyan", justify="left")
    table.add_column("내용", style=f"bold {order_color}", justify="right")

    table.add_row("거래종류", f"[{order_color}]{order_type}[/]")
    table.add_row("거래수량", f"[cyan]{USDT_quantity} USDT[/]")
    table.add_row("체결가격", f"[blue]{price:,} KRW[/]")
    table.add_row("거래금액", f"[bold yellow]{round(price * USDT_quantity):,} KRW[/]")

    # ✅ 주문 성공 여부 확인
    console.print("\n")
    if result["status"] == "0000":
        console.print(f"[bold {order_color}]✅ {order_type} 주문 성공![/]")
    else:
        console.print("[bold red]❌ 주문 실패![/]")
        console.print(json.dumps(result, indent=4, ensure_ascii=False))

    # 🎨 테이블 출력
    console.print("\n")
    console.print(table)
    console.print("\n")



def print_webhook_message(webhook_data):
    """
    웹훅 메시지를 터미널에 보기 좋게 출력하는 함수

    Parameters:
        webhook_data (dict): 웹훅에서 전달된 JSON 데이터
    """
    
    # 📌 웹훅 데이터가 딕셔너리가 아닐 경우 변환
    if isinstance(webhook_data, str):
        try:
            webhook_data = json.loads(webhook_data)
        except json.JSONDecodeError:
            console.print("[bold red]❌ 웹훅 데이터 오류: JSON 디코딩 실패![/]")
            return

    # 📌 웹훅 메시지 테이블 생성
    table = Table(title="📌 웹훅 메시지", show_header=True, header_style="bold magenta")
    table.add_column("키", style="cyan", justify="left")
    table.add_column("값", style="bold yellow", justify="right")

    # 📌 JSON 데이터를 테이블에 추가
    for key, value in webhook_data.items():
        table.add_row(key, str(value))

    # ✅ 웹훅 메시지 출력
    console.print("\n")
    console.print(table)
    console.print("\n")


def print_webhook_message2(webhook_data):
    """
    기본 print()로 터미널에서 안정적으로 출력하는 함수
    """
    if isinstance(webhook_data, str):
        try:
            webhook_data = json.loads(webhook_data)
        except json.JSONDecodeError:
            print("❌ 웹훅 데이터 오류: JSON 디코딩 실패!")
            return

    print("\n📌 최신 웹훅 메시지\n" + "="*40)

    # 키와 값의 정렬을 맞추기 위한 길이 설정
    max_key_length = max(len(key) for key in webhook_data.keys()) + 2  # 키 길이 맞추기
    for key, value in webhook_data.items():
        print(f"{key.ljust(max_key_length)}: {str(value).rjust(20)}")  # 정렬 유지

    print("="*40 + "\n")




if __name__ == "__main__":



    # 매수/매도 호가 조회
    #orderbook = get_orderbook("USDT")
    #print(orderbook)

    # 구매 가능한 USDT 수량 계산
    #USDT_quantity, price = get_market_price_units("USDT", percent=0.1)
    #print(USDT_quantity, price)


    # 내 자산 정보 조회
    #get_balance("USDT")

    print_order_info("buy", 100, 1500, {'status': '000'})
    print_order_info("sell", 100, 1500, {'status': '000'})