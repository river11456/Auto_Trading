import logging
from logging.handlers import RotatingFileHandler
import os
from app.config.config import settings


def setup_logger(log_name=None):
    """
    로거 설정 함수

    Parameters:
        log_name (str): 로거 이름 (None이면 기본 설정 사용)
    Returns:
        logging.Logger: 설정된 로거 객체
    """
    # logs 디렉토리 생성
    os.makedirs(settings.LOG_DIR, exist_ok=True)

    # 로거 이름 설정
    if log_name is None:
        log_name = "logger"

    # 로거 생성
    logger = logging.getLogger(log_name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

    # 포맷 정의
    log_format = logging.Formatter(settings.LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")

    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # 파일 핸들러 설정 (config에서 설정 가져오기)
    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    return logger


# 전역 로거 인스턴스 생성
logger = setup_logger()

trading_loger = setup_logger("trading_loger")
strategy_loger = setup_logger("strategy_loger")
bithumb_api_loger = setup_logger("bithumb_api_loger")




if __name__ == "__main__":
    logger.info("로거 설정 완료")
    logger.debug("디버그 메시지")
    logger.warning("경고 메시지")
    logger.error("에러 메시지")
    logger.critical("심각한 에러 메시지")