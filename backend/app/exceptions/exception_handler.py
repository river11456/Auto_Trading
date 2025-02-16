from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.utils.logger import logger
from app.exceptions.custom_exceptions import APIError, BusinessLogicError



async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    요청 데이터 검증 실패 시 호출되는 예외 처리 함수
    """
    logger.error(f"요청 데이터 검증 실패: {exc.errors()}")
    logger.error(f"요청 데이터: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    기타 예상치 못한 예외 발생 시 호출되는 예외 처리 함수
     
    Exception은 파이썬 기본 내장 예외를 모두 포함함

    """
    logger.error(f"서버 내부 오류 발생: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "서버 내부 오류가 발생했습니다."},
    )



async def api_error_handler(request: Request, exc: APIError):
    """외부 API 호출 실패 시 처리"""
    logger.error(f"API 오류 발생: {str(exc)}")
    return JSONResponse(
        status_code=502,  # Bad Gateway: 외부 API 실패
        content={"error": "API 호출 실패", "detail": str(exc)},
    )


async def business_logic_error_handler(request: Request, exc: BusinessLogicError):
    """비즈니스 로직 오류 시 처리"""
    logger.error(f"비즈니스 로직 오류: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"error": "비즈니스 로직 오류", "detail": str(exc)},
    )



