from my_bittmb_fnc import *
from fastapi import FastAPI, Request
import uvicorn
import json

app = FastAPI()

@app.post("/webhook")
async def webhook_handler(request: Request):

    try:
        data = await request.json()
    except Exception as e:
        print("JSON 파싱 에러:", e)
        return {"status": "error", "message": "유효하지 않은 JSON 데이터"}
    
    #print("Webhook received:\n", json.dumps(data, indent=4, ensure_ascii=False))


    # 신호에 따라 매수
    signal = data.get("signal")
    if signal is None:
        return {"status": "error", "message": "signal 필드가 없습니다."}    
    
    if signal == "buy":

        # 구매 가능한 USDT 수량 계산
        USDT_quantity = get_market_price_units("USDT", percent=0.1)
 
        # 시장가 전량 매수
        result = order_market_buy(USDT_quantity, "USDT", "KRW")
 
        # 거래가격 확인
        orderbook = get_orderbook("USDT")
        price = int(float(orderbook["data"]["asks"][0]["price"]))
    
        if result["status"] == "0000":
            print("🟢 시장가 매수 주문 성공")
            print(f"거래수량 : {USDT_quantity} USDT")
            print(f"체결가격 : {price} KRW")
            print(f"거래금액 : {int(price * USDT_quantity)} KRW")

        else:    
            print('🔴 시장가 매수 주문 실패')        


    elif signal == "sell":

        # 보유 중인 USDT 수량 조회
        balance = get_balance("USDT")
        USDT_quantity = float(balance["data"]["total_usdt"])

        # 시장가 전량 매도
        result = order_market_sell(USDT_quantity, "USDT", "KRW")

        # 거래가격 확인
        orderbook = get_orderbook("USDT")
        price = int(float(orderbook["data"]["bids"][0]["price"]))

        if result["status"] == "0000":  
            print("🟢 시장가 매도 주문 성공")
            print(f"거래수량 : {USDT_quantity} USDT")
            print(f"체결가격 : {price} KRW")
            print(f"거래금액 : {int(USDT_quantity * price)} KRW")
        else:
            print('🔴 시장가 매도 주문 실패')

    else:
        print("알 수 없는 신호입니다.")
        return {"status": "error", "message": "알 수 없는 신호입니다."}


    return {"status": "success", "message": "Webhook received", "data": data}




if __name__ == "__main__":
    # host="0.0.0.0"은 모든 네트워크 인터페이스에서 접근 가능하도록 하며,
    # port=8000은 로컬에서 사용할 포트 번호입니다.
    uvicorn.run(app, host="0.0.0.0", port=8000)
 






