import jwt
import uuid
import hashlib
import time
from urllib.parse import urlencode
import requests
import json
import os
from fastapi import FastAPI, Request
import uvicorn



"""
빗썸 API 2.0 사용 코드
API 2.0 은 고정 IP를 사용하기 때문에 유동 IP를 사용하는 경우에는 API 1.0을 사용해야 합니다.
"""


app = FastAPI()

# 빗썸 API 키 설정 (환경변수로부터 읽어옴)
BITHUMB_API_KEY = os.getenv('BITHUMB_API_KEY')
BITHUMB_SECRET = os.getenv('BITHUMB_SECRET')
BITHUMB_API_URL = 'https://api.bithumb.com'

def place_order(request_body: dict) -> None:
    """
    빗썸 API를 호출하여 주문을 실행하는 함수입니다.
    """
    # Generate access token
    # 요청 파라미터를 URL 인코딩하여 바이트 문자열로 변환
    query = urlencode(request_body).encode()
    
    # SHA512 해시 생성
    hash_obj = hashlib.sha512()
    hash_obj.update(query)
    query_hash = hash_obj.hexdigest()
    
    # JWT 페이로드 구성
    payload = {
        'access_key': BITHUMB_API_KEY,
        'nonce': str(uuid.uuid4()),
        'timestamp': round(time.time() * 1000),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }
    
    # JWT 토큰 생성 및 Bearer 토큰 구성
    jwt_token = jwt.encode(payload, BITHUMB_SECRET)
    authorization_token = f'Bearer {jwt_token}'
    
    # 요청 헤더 구성
    headers = {
        'Authorization': authorization_token,
        'Content-Type': 'application/json'
    }
    
    try:
        # API 호출
        response = requests.post(BITHUMB_API_URL + '/v1/orders',
                                 data=json.dumps(request_body),
                                 headers=headers)
        

        if request_body.get('side') == 'bid':
            side='매수'
        else:               
            side='매도'

        if request_body.get('ord_type') == 'price' or request_body.get('ord_type') == 'market':
            order_type = '시장가'
        else: 
            order_type = '지정가'


        if response.status_code == 201:
            print(f"🟢 주문 성공 : {order_type} {side}")
        else :
            print(f"🔴 주문 실패 : {order_type} {side}")
 

        print(json.dumps(response.json(), indent=4, ensure_ascii=False))


    except Exception as err:
        print("🔴 API 호출 중 에러 발생:", err)




def get_balance():
    # Generate access token
    payload = {
        'access_key': BITHUMB_API_KEY,
        'nonce': str(uuid.uuid4()),
        'timestamp': round(time.time() * 1000)
    }           
    jwt_token = jwt.encode(payload, BITHUMB_SECRET)
    authorization_token = 'Bearer {}'.format(jwt_token)
    headers = {
   'Authorization': authorization_token
    }

    try:
        # Call API
        response = requests.get(BITHUMB_API_URL + '/v1/accounts', headers=headers)
        # handle to success or fail
        # print(response.status_code)
        # print(json.dumps(response.json(), indent=4, ensure_ascii=False))
        return response.json()
    except Exception as err:
        # handle exception
        print(err)





@app.post("/webhook")
async def webhook_handler(request: Request):

    try:
        data = await request.json()
    except Exception as e:
        print("JSON 파싱 에러:", e)
        return {"status": "error", "message": "유효하지 않은 JSON 데이터"}
    
    
    print("Webhook received:\n", json.dumps(data, indent=4, ensure_ascii=False))



    # 잔액 조회
    balance_data = get_balance()

    # USDT, KRW의 balance 정보를 찾기
    usdt_balance = None
    for asset in balance_data:
        if asset.get("currency") == "USDT":
            usdt_balance = asset.get("balance")
        if asset.get("currency") == "KRW":
            KRW_balance = asset.get("balance")

    if KRW_balance is not None:
        KRW_balance = int(float(KRW_balance)*0.99)

    print(f'USDT 잔액 : {usdt_balance}')
    print(f'KRW 잔액 : {KRW_balance}')

    final_price = KRW_balance * 0.1

    # 신호에 따라 매수
    signal = data.get("signal")
    if signal is None:
        return {"status": "error", "message": "signal 필드가 없습니다."}    
    
    if signal == "buy":
        request_body = dict( market='KRW-USDT', side='bid', price=final_price, ord_type='price' )
        place_order(request_body)
    elif signal == "sell":
        request_body = dict( market='KRW-USDT', side='ask', volume=usdt_balance, ord_type='market' )
        place_order(request_body)
    else:
        print("알 수 없는 신호입니다.")
        return {"status": "error", "message": "알 수 없는 신호입니다."}





    return {"status": "success", "message": "Webhook received", "data": data}






if __name__ == '__main__':

    uvicorn.run(app, host="0.0.0.0", port=8000)
