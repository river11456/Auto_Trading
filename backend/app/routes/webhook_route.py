from fastapi import APIRouter, HTTPException
from app.models.trading_model import TradeRequest, TradeResponse
from app.services.trading_service import execute_trade
from app.utils.logger import logger
from app.utils.display import display_trade_request, display_trade_response
from app.utils.display import display_log

# 라우터 인스턴스 생성
router = APIRouter()


@router.post("/webhook", response_model=TradeResponse)
async def handle_webhook(request: TradeRequest):
    """
    TradingView 웹훅 요청 처리 라우트

    - 요청 데이터는 `TradeRequest` 모델로 검증
    - 트레이딩 서비스(`execute_trade`)를 호출하여 매수/매도 실행
    - 응답 데이터는 `TradeResponse` 모델로 반환
    """

    # 웹훅 수신 로그 출력
    logger.info(f"웹훅 요청 수신: {request.model_dump()}")
    

    # 요청 데이터 유효성 검증
    if request.signal not in {"buy", "sell", "test"}:
        raise HTTPException(status_code=400, detail="잘못된 signal 값입니다. 'buy' 또는 'sell'만 허용됩니다.")

    # 트레이딩 서비스 실행
    try:
        trade_response = execute_trade(request)
        logger.info(f"거래 실행 결과: {trade_response.model_dump()}")
        return trade_response

    except Exception as e:
        logger.error(f"거래 실행 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류")


# `/webhook` 이외의 요청은 모두 차단
@router.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def block_other_routes(full_path: str):
    raise HTTPException(status_code=403, detail="허용되지 않은 접근입니다.")
