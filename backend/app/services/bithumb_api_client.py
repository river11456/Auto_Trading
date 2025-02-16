import time
import math
import base64
import hmac, hashlib
import urllib.parse
import requests
from typing import Optional
from app.config.config import settings
from app.exceptions.custom_exceptions import APIError
from app.models.trading_model import (
    TickerResponse, OrderbookResponse, BalanceResponse, TransactionResponse
)

class XCoinAPI:
    """
    빗썸 API 인증 및 요청 클래스
    """
    api_url = settings.BITHUMB_API_URL

    def __init__(self, api_key: str, api_secret: str):
        if not api_key or not api_secret:
            raise ValueError("API 키 또는 시크릿이 설정되어 있지 않습니다.")
        self.api_key = api_key
        self.api_secret = api_secret

    def microtime(self, get_as_float=False):
        return time.time() if get_as_float else '%f %d' % math.modf(time.time())

    def usecTime(self):
        mt = self.microtime(False)
        mt_array = mt.split(" ")[:2]
        return mt_array[1] + mt_array[0][2:5]

    def xcoinApiCall(self, endpoint, rgParams):

        #빗썸 API 호출 함수
        str_data = urllib.parse.urlencode(rgParams)
        nonce = self.usecTime()
        data = endpoint + chr(0) + str_data + chr(0) + nonce
        utf8_data = data.encode('utf-8')

        utf8_key = self.api_secret.encode('utf-8')
        h = hmac.new(utf8_key, utf8_data, hashlib.sha512)
        api_sign = base64.b64encode(h.hexdigest().encode('utf-8')).decode('utf-8')

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Api-Key": self.api_key,
            "Api-Nonce": nonce,
            "Api-Sign": api_sign
        }

        url = f"{self.api_url}{endpoint}"
        response = requests.post(url, headers=headers, data=rgParams)
        return response.json()


# XCoinAPI 인스턴스 생성 (config에서 API 키 불러오기)
client = XCoinAPI(settings.BITHUMB_API_KEY, settings.BITHUMB_SECRET)


def api_request(endpoint: str, method: str = "GET", payload: Optional[dict] = None):
    """
    빗썸 API 호출을 위한 공통 함수
    """
    url = f"{settings.BITHUMB_API_URL}{endpoint}"
    headers = {"accept": "application/json"}

    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
            result = response.json()
        elif method == "POST":
            result = client.xcoinApiCall(endpoint, payload)
        else:
            raise APIError(f"지원되지 않는 HTTP 메서드: {method}")

        if result.get("status") != "0000":
            raise APIError(f"{result.get('message', '알 수 없는 오류')}")
        return result

    except requests.exceptions.RequestException as e:
        raise APIError(f"네트워크 오류로 API 요청 실패: {str(e)}")

    except Exception as e:
        raise RuntimeError(f"API 요청 실패: {e}")


def get_ticker(order_currency: str, payment_currency: str = "KRW") -> TickerResponse:
    response = api_request(f"/public/ticker/{order_currency}_{payment_currency}", "GET")
    return TickerResponse(status=response["status"], **response["data"])

def get_orderbook(order_currency: str, payment_currency: str = "KRW") -> OrderbookResponse:
    response = api_request(f"/public/orderbook/{order_currency}_{payment_currency}", "GET")
    return OrderbookResponse(status=response["status"], **response["data"])

def get_balance(currency: str) -> BalanceResponse:
    payload = {"currency": currency}
    response = api_request("/info/balance", "POST", payload)
    return BalanceResponse.from_api_response(response,currency)

def order_market_buy(units: float, order_currency: str, payment_currency: str = "KRW"):
    payload = {"units": units, "order_currency": order_currency, "payment_currency": payment_currency}
    return api_request("/trade/market_buy", "POST", payload)

def order_market_sell(units: float, order_currency: str, payment_currency: str = "KRW"):
    payload = {"units": units, "order_currency": order_currency, "payment_currency": payment_currency}
    return api_request("/trade/market_sell", "POST", payload)

def get_user_transactions(order_currency: str, payment_currency: str = "KRW", count: int = 20, offset: int = 0, searchGb: int = 0) -> TransactionResponse:
    payload = {
        "order_currency": order_currency,
        "payment_currency": payment_currency,
        "count": count,
        "offset": offset,
        "searchGb": searchGb
    }
    response = api_request("/info/user_transactions", "POST", payload)
    return TransactionResponse.from_api_response(response)
