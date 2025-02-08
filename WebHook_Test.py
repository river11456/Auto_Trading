from fastapi import FastAPI, Request
import uvicorn
import json

app = FastAPI()

@app.post("/webhook")
async def webhook_handler(request: Request):
    """
    TradingView 웹훅으로부터 POST 요청을 받아 JSON 데이터를 출력하고,
    간단한 응답을 반환하는 엔드포인트입니다.
    """
    try:
        data = await request.json()
    except Exception as e:
        print("JSON 파싱 에러:", e)
        return {"status": "error", "message": "유효하지 않은 JSON 데이터"}


    print("Webhook received:\n", json.dumps(data, indent=4, ensure_ascii=False))
    return {"status": "success", "message": "Webhook received", "data": data}

if __name__ == "__main__":
    # host="0.0.0.0"은 모든 네트워크 인터페이스에서 접근 가능하도록 하며,
    # port=8000은 로컬에서 사용할 포트 번호입니다.
    uvicorn.run(app, host="0.0.0.0", port=8000)
