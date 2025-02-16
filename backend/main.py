import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.routes.webhook_route import router as webhook_router
from app.utils.logger import logger
from app.config.config import settings
from app.utils.nginx_checker import check_and_start_nginx
from app.utils.process_checker import find_and_kill_process
from app.exceptions.exception_handler import validation_exception_handler, general_exception_handler




app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.include_router(webhook_router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)



if __name__ == "__main__":
    # ✅ 서버 시작 준비 로깅
    logger.info("🚀 서버 시작 준비 중...")

    # Nginx 상태 확인 후 필요 시 실행
    check_and_start_nginx()

    # FastAPI 실행 전 사용 중인 포트 프로세스 종료
    find_and_kill_process(settings.FASTAPI_PORT)

    logger.info("✅ FastAPI 서버가 성공적으로 시작되었습니다!")

    # FastAPI 서버 실행
    uvicorn.run(app, host=settings.FASTAPI_HOST, port=settings.FASTAPI_PORT)
