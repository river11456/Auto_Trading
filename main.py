from mylib import *
from fastapi import FastAPI, Request, HTTPException
import uvicorn
import json
import logging

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# 로거 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


#매수/매도할 자산 비율 (0~1)
BUY_PERCENT = 0.01  # KRW의 1% 매수
SELL_PERCENT = 1  # 테더 전량 매도




@app.post("/webhook")
async def webhook_handler(request: Request):

    try:
        webhook_data = await request.json()
    except Exception as e:
        print("JSON 파싱 에러:", e)
        return {"status": "error", "message": "유효하지 않은 JSON 데이터"}
    

     # ✅ 웹훅 메시지를 로깅 (print 대신 logger 사용)
    print('\n')
    logger.info(f"웹훅 데이터 수신")
    
    # 웹훅 메시지 출력
    print_webhook_message(webhook_data)


    # 신호에 따라 매수
    signal = webhook_data.get("signal")
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
        print("매수 또는 매도 신호가 아닙니다.\n")
        return {"status": "error", "message": "매수 또는 매도 신호가 아닙니다."}


    return {"status": "success", "message": "Webhook received", "webhook_data": webhook_data}



# `/webhook` 외 모든 요청을 차단
@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def block_other_routes(full_path: str):
    raise HTTPException(status_code=403, detail="Access Denied")



if __name__ == "__main__":
    # FastAPI 서버를 로컬에서만 실행 (Nginx가 외부 요청을 대신 처리)
    uvicorn.run(app, host="127.0.0.1", port=8000)
 






