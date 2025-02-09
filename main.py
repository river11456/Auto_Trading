from mylib import *
from fastapi import FastAPI, Request
import uvicorn
import json

app = FastAPI()


#매수/매도할 자산 비율 (0~1)
BUY_PERCENT = 0.01
SELL_PERCENT = 1


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

        # 매수할 USDT 수량 계산
        USDT_quantity, price = make_order_info(signal, "USDT", percent=BUY_PERCENT)
 
        # 시장가 전량 매수
        result = order_market_buy(USDT_quantity, "USDT", "KRW")
 
        print_order_info(signal, USDT_quantity, price, result)     


    elif signal == "sell":

        # 매도할 USDT 수량 계산
        USDT_quantity, price = make_order_info(signal, "USDT", percent=SELL_PERCENT)

        # 시장가 전량 매도
        result = order_market_sell(USDT_quantity, "USDT", "KRW")

        print_order_info(signal, USDT_quantity, price, result)

    else:
        print("알 수 없는 신호입니다.")
        return {"status": "error", "message": "알 수 없는 신호입니다."}


    return {"status": "success", "message": "Webhook received", "data": data}




if __name__ == "__main__":
    # host="0.0.0.0"은 모든 네트워크 인터페이스에서 접근 가능하도록 하며,
    # port=8000은 로컬에서 사용할 포트 번호입니다.
    uvicorn.run(app, host="0.0.0.0", port=8000)
 






