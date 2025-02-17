import os
import re
import logging
from logging.handlers import RotatingFileHandler
from app.utils.display import display_log
from app.config.config import settings





# 터미널에서 보기 좋게 출력하기 위한 커스텀 핸들러  
# 기존 핸들러의 출력을 인자로 사용해서 출력
class ConsoleHandlerWithDisplay(logging.StreamHandler):
    """기존 핸들러 출력 후 display_log()를 호출하는 콘솔 핸들러"""

    def emit(self, record):
        try:
            if record.levelno >= logging.INFO:
                log_entry = self.format(record) # 기존 핸들러 출력 
                #super().emit(record)  # 원래 콘솔에 출력

                # Enum 변환 적용
                log_entry = sanitize_log_entry(log_entry)

                display_log(log_entry)

        except Exception as e:
            print(f"로그 출력 중 오류 발생: {str(e)}")


def sanitize_log_entry(log_entry: str) -> str:
    """
    로그 메시지에서 Enum 형식 (<EnumType.VALUE: 'value'>)을 단순한 문자열로 변환.
    """
    return re.sub(r"<\w+\.\w+: '([^']+)'>", r"'\1'", log_entry)  # Enum을 일반 문자열로 변환


def setup_logger():
    """로거 설정"""
    # logs 디렉토리 생성
    os.makedirs(settings.LOG_DIR, exist_ok=True)

    # 기본 로거 가져오기
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))


    # 포맷 정의 
    log_format = logging.Formatter(settings.LOG_FORMAT)

    # 콘솔 핸들러 설정
    #console_handler = logging.StreamHandler()  <- 기본 출력 핸들러
    console_handler = ConsoleHandlerWithDisplay()  #display를 위한 커스텀 핸들러
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # 파일 핸들러 설정
    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(settings.LOG_LEVEL)
    logger.addHandler(file_handler)

    return logger



# 전역 로거 인스턴스 생성
logger = setup_logger()


if __name__ == "__main__":
    logger.info("로거 설정 완료")
    logger.debug("디버그 메시지")
    logger.warning("경고 메시지")
    logger.error("에러 메시지")
    logger.critical("심각한 에러 메시지")